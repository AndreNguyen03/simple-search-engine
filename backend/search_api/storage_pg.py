import psycopg2
import config

def get_conn():
    print(f"[Storage] Connecting to PostgreSQL at {config.PG_HOST}:{config.PG_PORT} with user {config.PG_USER} {config.PG_PASSWORD}")
    return psycopg2.connect(
        dbname=config.PG_DB,
        user=config.PG_USER,
        password=config.PG_PASSWORD,
        host=config.PG_HOST,
        port=config.PG_PORT
    )

def init_db():
    with get_conn() as conn:
        with conn.cursor() as c:
            c.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    url TEXT UNIQUE,
                    title TEXT,
                    content TEXT,
                    visited BOOLEAN DEFAULT FALSE,
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

def insert_document(url: str, content: str, title: str):
    try:
        conn = get_conn()
        with conn.cursor() as cursor:
            cursor.execute(
                'INSERT INTO documents (url, content, title, visited) VALUES (%s, %s, %s, TRUE)',
                (url, content, title)
            )
            conn.commit()
        conn.close()
        print(f"[Storage] ✅ Đã insert vào database: {url}")
    except Exception as e:
        print(f"[Storage] ❌ Lỗi insert document {url}: {e}")

def get_unvisited_documents():
    with get_conn() as conn:
        with conn.cursor() as c:
            c.execute('SELECT id, url, title, content FROM documents WHERE visited = TRUE AND length = 0')
            return c.fetchall()

def update_doc_length(doc_id: int, length: float):
    with get_conn() as conn:
        with conn.cursor() as c:
            c.execute('UPDATE documents SET length = %s WHERE id = %s', (length, doc_id))
        conn.commit()

def upsert_index(term: str, doc_id: int, freq: int):
    with get_conn() as conn:
        with conn.cursor() as c:
            c.execute('''
                INSERT INTO inverted_index (term, doc_id, freq, df)
                VALUES (%s, %s, %s, 1)
                ON CONFLICT (term, doc_id)
                DO UPDATE SET freq = EXCLUDED.freq
            ''', (term, doc_id, freq))
        conn.commit()

def update_df(term: str):
    with get_conn() as conn:
        with conn.cursor() as c:
            c.execute('''
                UPDATE inverted_index SET df = (
                    SELECT COUNT(*) FROM inverted_index AS ii
                    WHERE ii.term = inverted_index.term
                ) WHERE term = %s
            ''', (term,))
        conn.commit()

def get_df(term: str) -> int:
    with get_conn() as conn:
        with conn.cursor() as c:
            c.execute('SELECT df FROM inverted_index WHERE term = %s LIMIT 1', (term,))
            result = c.fetchone()
            return result[0] if result else 0

def count_documents() -> int:
    with get_conn() as conn:
        with conn.cursor() as c:
            c.execute('SELECT COUNT(*) FROM documents')
            return c.fetchone()[0]

def get_inverted_index() -> dict:
    index = {}
    with get_conn() as conn:
        with conn.cursor() as c:
            c.execute('SELECT term, doc_id, freq, df FROM inverted_index')
            for term, doc_id, freq, df in c.fetchall():
                if term not in index:
                    index[term] = {'df': df, 'postings_list': {}}
                index[term]['postings_list'][doc_id] = freq
    return index

def get_document(doc_id: int) -> dict:
    with get_conn() as conn:
        with conn.cursor() as c:
            c.execute('SELECT id, url, title, content FROM documents WHERE id = %s', (doc_id,))
            row = c.fetchone()
            if row:
                return {'id': row[0], 'url': row[1], 'title': row[2], 'content': row[3]}
            return {}

def get_doc_length(doc_id: int) -> float:
    with get_conn() as conn:
        with conn.cursor() as c:
            c.execute('SELECT length FROM documents WHERE id = %s', (doc_id,))
            result = c.fetchone()
            return result[0] if result and result[0] else 0.0

def upsert_index_batch(records: list[tuple[str, int, int]]):
    sql = '''
        INSERT INTO inverted_index (term, doc_id, freq, df)
        VALUES (%s, %s, %s, 1)
        ON CONFLICT (term, doc_id)
        DO UPDATE SET freq = EXCLUDED.freq
    '''
    with get_conn() as conn:
        with conn.cursor() as c:
            c.executemany(sql, records)
        conn.commit()
        print(f"[Storage] ✅ Đã upsert {len(records)} records vào inverted_index.")

def get_df_batch(terms: list[str]) -> dict[str, int]:
    if not terms:
        return {}

    placeholders = ','.join(['%s'] * len(terms))
    query = f'''
        SELECT term, MAX(df) as df
        FROM inverted_index
        WHERE term IN ({placeholders})
        GROUP BY term
    '''
    with get_conn() as conn:
        with conn.cursor() as c:
            c.execute(query, terms)
            rows = c.fetchall()
    return {term: df for term, df in rows}

def get_doc_lengths(doc_ids: list[int]) -> dict[int, float]:
    if not doc_ids:
        return {}

    placeholders = ','.join(['%s'] * len(doc_ids))
    query = f'''
        SELECT id, length FROM documents
        WHERE id IN ({placeholders})
    '''
    with get_conn() as conn:
        with conn.cursor() as c:
            c.execute(query, doc_ids)
            rows = c.fetchall()
    return {doc_id: length for doc_id, length in rows}