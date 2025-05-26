import math
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import storage_pg
import helper
from stopwords import STOPWORDS_SET


def process_doc(doc):
    doc_id, url, title, content = doc
    tokens = helper.preprocess_text(content, STOPWORDS_SET)
    bow = Counter(tokens)
    return doc_id, url, bow


def index_documents():
    documents = storage_pg.get_unvisited_documents()
    if not documents:
        print("📭 Không có văn bản mới để index.")
        return

    num_docs = storage_pg.count_documents()
    print(f"📄 Tổng văn bản: {num_docs}")

    index_data = defaultdict(list)  # term -> [(doc_id, freq), ...]
    doc_bows = {}  # doc_id -> bow
    docs_info = {}  # doc_id -> url

    # 1. Xử lý song song để lấy bow của từng doc
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_doc, doc) for doc in documents]
        for future in as_completed(futures):
            doc_id, url, bow = future.result()
            doc_bows[doc_id] = bow
            docs_info[doc_id] = url
            for term, freq in bow.items():
                index_data[term].append((doc_id, freq))

    # 2. Tính DF mới của batch (số doc chứa term trong batch này)
    batch_df = {term: len(postings) for term, postings in index_data.items()}

    # 3. Lấy DF hiện có của term trong DB bằng batch query
    terms = list(batch_df.keys())
    df_existing = storage_pg.get_df_batch(terms)  # bạn cần implement hàm này trong storage

    # 4. Tổng DF = DF cũ + DF batch
    df_total = {term: df_existing.get(term, 0) + batch_df[term] for term in batch_df.keys()}

    # 5. Chuẩn bị dữ liệu batch để upsert (term, doc_id, freq)
    upsert_records = []
    for term, postings in index_data.items():
        for doc_id, freq in postings:
            upsert_records.append((term, doc_id, freq))

    # 6. Thực hiện batch upsert
    storage_pg.upsert_index_batch(upsert_records)  # bạn cần implement hàm này trong storage

    # 7. Cập nhật df cho từng term (vẫn chạy từng term, có thể batch update nếu muốn)
    for term, df in df_total.items():
        storage_pg.update_df(term)

    # 8. Tính TF-IDF vector và length cho từng document, update length
    for doc_id, bow in doc_bows.items():
        vector = []
        for term, freq in bow.items():
            tf = helper.tf(freq)
            idf = helper.idf(df_total.get(term, 1), num_docs)
            vector.append(tf * idf)
        length = math.sqrt(sum(w ** 2 for w in vector))
        storage_pg.update_doc_length(doc_id, length)
        print(f"🔍 Đã index: {docs_info[doc_id]} (id={doc_id}, length={length:.2f})")

    print("✅ Indexing hoàn tất.")
