import sqlite3
import config 

def get_conn():
    print(f"[Storage] ✅ Kết nối tới database: {config.DB_PATH}")
    return sqlite3.connect(config.DB_PATH)

def init_db():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                content TEXT,
                visited INTEGER DEFAULT 0,
                length REAL DEFAULT 0
            );
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS inverted_index (
                term TEXT,
                doc_id INTEGER,
                freq INTEGER,
                df INTEGER DEFAULT 1,
                PRIMARY KEY (term, doc_id)
            );
        ''')
        conn.commit()

# ================= CRAWLER ==================

def insert_document(url: str, content: str):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO documents (url, content, visited) VALUES (?, ?, 1)',
            (url, content)
        )
        conn.commit()
        conn.close()
        print(f"[Storage] ✅ Đã insert vào database: {url}")
    except Exception as e:
        print(f"[Storage] ❌ Lỗi insert document {url}: {e}")

def get_unvisited_documents():
    with get_conn() as conn:
        c = conn.cursor()
        return c.execute('SELECT id, url, content FROM documents WHERE visited = 1 AND length = 0').fetchall()

# ================= INDEXING ==================

def update_doc_length(doc_id: int, length: float):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('UPDATE documents SET length = ? WHERE id = ?', (length, doc_id))
        conn.commit()

def upsert_index(term: str, doc_id: int, freq: int):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO inverted_index (term, doc_id, freq, df)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(term, doc_id)
            DO UPDATE SET freq=excluded.freq
        ''', (term, doc_id, freq))
        conn.commit()

def update_df(term: str):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('''
            UPDATE inverted_index SET df = (
                SELECT COUNT(*) FROM inverted_index AS ii
                WHERE ii.term = inverted_index.term
            ) WHERE term = ?
        ''', (term,))
        conn.commit()
        
def get_df(term: str) -> int:
    with get_conn() as conn:
        c = conn.cursor()
        result = c.execute('SELECT df FROM inverted_index WHERE term = ? LIMIT 1', (term,)).fetchone()
        return result[0] if result else 0

def count_documents() -> int:
    with get_conn() as conn:
        c = conn.cursor()
        return c.execute('SELECT COUNT(*) FROM documents').fetchone()[0]

def get_inverted_index() -> dict:
    """
    Trả về toàn bộ inverted index dưới dạng:
    {
        term1: {
            'df': int,
            'postings_list': {doc_id1: freq, doc_id2: freq, ...}
        },
        ...
    }
    """
    index = {}
    with get_conn() as conn:
        c = conn.cursor()
        rows = c.execute('SELECT term, doc_id, freq, df FROM inverted_index').fetchall()
        for term, doc_id, freq, df in rows:
            if term not in index:
                index[term] = {
                    'df': df,
                    'postings_list': {}
                }
            index[term]['postings_list'][doc_id] = freq
    return index

def get_document(doc_id: int) -> dict:
    """
    Trả về 1 document dưới dạng dict: {'id': ..., 'url': ..., 'content': ...}
    """
    with get_conn() as conn:
        c = conn.cursor()
        row = c.execute('SELECT id, url, content FROM documents WHERE id = ?', (doc_id,)).fetchone()
        if row:
            return {
                'id': row[0],
                'url': row[1],
                'content': row[2]
            }
        return {}
    
def get_doc_length(doc_id: int) -> float:
    """
    Trả về chiều dài (norm) của document
    """
    with get_conn() as conn:
        c = conn.cursor()
        result = c.execute('SELECT length FROM documents WHERE id = ?', (doc_id,)).fetchone()
        return result[0] if result and result[0] else 0.0
