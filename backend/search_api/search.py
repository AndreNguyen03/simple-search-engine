import math
from collections import defaultdict, Counter
from typing import List
from storage import (
    get_inverted_index, get_document, get_doc_length, count_documents
)
from stopwords import STOPWORDS_SET
from helper import tf, idf,preprocess_text
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from search_api.models import SearchResult
import time

def search(query: str, top_k: int = 20, page: int = 1) -> List[SearchResult]:
    start_time = time.time()
    # Lấy dữ liệu
    index_db = get_inverted_index()
    num_docs = count_documents()
    vocabulary = set(index_db.keys())

    # Tiền xử lý truy vấn
    tokens = preprocess_text(query, STOPWORDS_SET)
    tokens = [token for token in tokens if token in vocabulary]
    if not tokens:
         return [], 0, round(time.time() - start_time, 2)

    # TF-IDF cho truy vấn
    query_bow = Counter(tokens)
    query_weights = {}
    for term, freq in query_bow.items():
        df = index_db[term]['df']
        query_weights[term] = tf(freq) * idf(df, num_docs)

    # Chuẩn hóa vector truy vấn
    query_length = math.sqrt(sum(w ** 2 for w in query_weights.values()))
    if query_length == 0:
        return []

    for term in query_weights:
        query_weights[term] /= query_length

    # Tính điểm cosine similarity
    scores = defaultdict(float)
    for term, q_weight in query_weights.items():
        df = index_db[term]['df']
        postings = index_db[term]['postings_list']
        for doc_id, tf_value in postings.items():
            doc_tf_idf = tf(tf_value) * idf(df, num_docs)
            doc_length = get_doc_length(doc_id)
            if doc_length > 0:
                scores[doc_id] += (q_weight * doc_tf_idf) / doc_length

    # Sắp xếp theo điểm
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    total_matches = len(sorted_docs)
    # Phân trang
    start = (page - 1) * top_k
    end = start + top_k
    paged_docs = sorted_docs[start:end]

    results: List[SearchResult] = []
    for doc_id, score in paged_docs:
        doc = get_document(doc_id)
        print(doc)
        snippet = doc['content'][:400] + "..." if doc and 'content' in doc else ""
        results.append({
            'doc_id': doc_id,
            'url': doc.get('url', ''),
            'title': doc.get('title', ''),
            'snippet': snippet,
            'score': round(score, 6)
        })

    elapsed_time = time.time() - start_time  # Tính thời gian
    return results, total_matches, elapsed_time