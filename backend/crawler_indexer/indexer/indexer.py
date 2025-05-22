# indexer.py

import math
from collections import Counter
from .. import storage
from .. import helper
from ...stopwords import STOPWORDS_SET


def index_documents():
    documents = storage.get_unvisited_documents()
    if not documents:
        print("📭 Không có văn bản mới để index.")
        return

    num_docs = storage.count_documents()
    print(f"📄 Số văn bản hiện tại: {num_docs}")

    for doc_id, url, content in documents:
        tokens = helper.preprocess_text(content, STOPWORDS_SET)
        bow = Counter(tokens)

        for term, freq in bow.items():
            storage.upsert_index(term, doc_id, freq)
            storage.update_df(term)

        # TF-IDF vector
        vector = []
        for term, freq in bow.items():
            df = storage.get_df(term)
            weight = helper.tf(freq) * helper.idf(df, num_docs)
            vector.append(weight)

        length = math.sqrt(sum(w ** 2 for w in vector))
        storage.update_doc_length(doc_id, length)

        print(f"🔍 Đã index: {url} (id={doc_id}, length={length:.2f})")

    print("✅ Indexing hoàn tất.")
