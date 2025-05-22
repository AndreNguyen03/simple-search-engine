from storage import init_db
from crawler_indexer.vietnamnet_crawler import crawler as vietnamnet_crawler
from crawler_indexer.indexer import indexer


if __name__ == '__main__':
    init_db()
    vietnamnet_crawler.crawl_and_insert()
    indexer.index_documents()
    print("✅ Done crawling and inserting.")
