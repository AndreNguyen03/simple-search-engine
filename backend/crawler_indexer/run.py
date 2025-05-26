import storage_pg
from vietnamnet_crawler import crawler as vietnamnet_crawler
from indexer import indexer


if __name__ == '__main__':
    storage_pg.init_db()
    vietnamnet_crawler.crawl_and_insert()
    indexer.index_documents()
    print("✅ Done crawling and inserting.")
