import math
from collections import defaultdict, Counter
from typing import List
import storage_pg
import stopwords
from helper import preprocess_text, tf, idf
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import SearchResult
import time

def search(query: str, top_k: int = 20, page: int = 1) -> List[SearchResult]:
    start_time = time.time()
    print(f"Starting search for query: '{query}', top_k: {top_k}, page: {page}")

    # Lấy dữ liệu
    index_db = storage_pg.get_inverted_index()
    print(f"Loaded {len(index_db)} terms in inverted index")
    num_docs = storage_pg.count_documents()
    print(f"Total documents in database: {num_docs}")
    vocabulary = set(index_db.keys())
    print(f"Vocabulary size: {len(vocabulary)}")

    # Tiền xử lý truy vấn
    tokens = preprocess_text(query, stopwords.STOPWORDS_SET)
    print(f"stopwrods: {len(stopwords.STOPWORDS_SET)}")
    print(f"Preprocessed query tokens: {tokens}")
    tokens = [token for token in tokens if token in vocabulary]
    print(f"Filtered tokens (in vocabulary): {tokens}")
    if not tokens:
        print("No valid tokens found in query after filtering")
        return [], 0, round(time.time() - start_time, 2)

    all_doc_ids = set()
    for term in tokens:
        doc_ids = index_db[term]['postings_list'].keys()
        print(f"Term '{term}' found in {len(doc_ids)} documents")
        all_doc_ids.update(doc_ids)
    print(f"Total unique document IDs matching query: {len(all_doc_ids)}")

    doc_lengths = storage_pg.get_doc_lengths(list(all_doc_ids))
    print(f"Retrieved document lengths for {len(doc_lengths)} documents")

    # TF-IDF cho truy vấn
    query_bow = Counter(tokens)
    print(f"Query bag-of-words: {dict(query_bow)}")
    query_weights = {}
    for term, freq in query_bow.items():
        df = index_db[term]['df']
        query_weights[term] = tf(freq) * idf(df, num_docs)
        print(f"Term '{term}': freq={freq}, df={df}, tf-idf={query_weights[term]:.6f}")

    # Chuẩn hóa vector truy vấn
    query_length = math.sqrt(sum(w ** 2 for w in query_weights.values()))
    print(f"Query vector length (before normalization): {query_length:.6f}")
    if query_length == 0:
        print("Query vector length is zero, returning empty results")
        return [], 0, round(time.time() - start_time, 2)

    for term in query_weights:
        query_weights[term] /= query_length
        print(f"Normalized weight for term '{term}': {query_weights[term]:.6f}")

    # Tính điểm cosine similarity
    scores = defaultdict(float)
    for term, q_weight in query_weights.items():
        df = index_db[term]['df']
        postings = index_db[term]['postings_list']
        print(f"Processing term '{term}' with df={df}, {len(postings)} postings")
        for doc_id, tf_value in postings.items():
            doc_tf_idf = tf(tf_value) * idf(df, num_docs)
            doc_length = doc_lengths.get(doc_id, 0)
            if doc_length > 0:
                score_contrib = (q_weight * doc_tf_idf) / doc_length
                scores[doc_id] += score_contrib
                print(f"Doc {doc_id}: tf={tf_value}, tf-idf={doc_tf_idf:.6f}, doc_length={doc_length:.6f}, score_contrib={score_contrib:.6f}")

    # Sắp xếp theo điểm
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    total_matches = len(sorted_docs)
    print(f"Total matching documents: {total_matches}")
    print(f"Top 5 document scores: {[(doc_id, round(score, 6)) for doc_id, score in sorted_docs[:5]]}")

    # Phân trang
    start = (page - 1) * top_k
    end = start + top_k
    paged_docs = sorted_docs[start:end]
    print(f"Paging: start={start}, end={end}, retrieved {len(paged_docs)} documents")

    results: List[SearchResult] = []
    for doc_id, score in paged_docs:
        doc = storage_pg.get_document(doc_id)
        print(f"Retrieved document {doc_id}: {doc}")
        snippet = doc['content'][:200] + "..." if doc and 'content' in doc else ""
        results.append({
            'doc_id': doc_id,
            'url': doc.get('url', ''),
            'title': doc.get('title', ''),
            'snippet': snippet,
            'score': round(score, 6)
        })
        print(f"Added result: doc_id={doc_id}, score={score:.6f}, url={doc.get('url', '')}")

    elapsed_time = time.time() - start_time
    print(f"Search completed in {elapsed_time:.2f} seconds")
    return results, total_matches, elapsed_time