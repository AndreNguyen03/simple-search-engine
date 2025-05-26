import unittest
from unittest.mock import patch, MagicMock
from vietnamnet_crawler.crawler import crawl_and_insert, is_url_visited, insert_document
from indexer.indexer import index_documents
from storage_pg import init_db
import run

class TestCrawlerIndexer(unittest.TestCase):
    def setUp(self):
        # Mock các hàm trong storage_pg
        self.mock_get_conn = patch('storage_pg.get_conn').start()
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_get_conn.return_value.__enter__.return_value = self.mock_conn
        self.mock_conn.cursor.return_value.__enter__.return_value = self.mock_cursor

    def tearDown(self):
        # Dừng tất cả các patch
        patch.stopall()

    @patch('common.extract_sitemaps')
    @patch('common.extract_urls_from_sitemap')
    @patch('vietnamnet_crawler.craw_helper.extract_text_from_url')
    @patch('vietnamnet_crawler.crawler.insert_document')
    @patch('vietnamnet_crawler.crawler.is_url_visited')  # Thêm mock cho is_url_visited
    @patch('storage_pg.get_unvisited_documents')
    @patch('storage_pg.count_documents')
    @patch('storage_pg.get_df_batch')
    @patch('storage_pg.upsert_index_batch')
    @patch('storage_pg.update_df')
    @patch('storage_pg.update_doc_length')
    def test_crawl_and_index_success(
        self,
        mock_update_doc_length,
        mock_update_df,
        mock_upsert_index_batch,
        mock_get_df_batch,
        mock_count_documents,
        mock_get_unvisited_documents,
        mock_is_url_visited,
        mock_insert_document,
        mock_extract_text_from_url,
        mock_extract_urls_from_sitemap,
        mock_extract_sitemaps
    ):
        # Mock dữ liệu trả về từ các hàm
        mock_extract_sitemaps.return_value = [
            f'http://example.com/sitemap{i}.xml' for i in range(6)
        ]
        mock_extract_urls_from_sitemap.return_value = ['http://example.com/page1']
        mock_is_url_visited.return_value = False  # URL chưa được visited
        mock_extract_text_from_url.return_value = ('Title 1', 'Content 1')
        mock_get_unvisited_documents.return_value = [(1, 'http://example.com/page1', 'Title 1', 'Content 1')]
        mock_count_documents.return_value = 1
        mock_get_df_batch.return_value = {'word1': 1}
        mock_upsert_index_batch.return_value = None
        mock_update_df.return_value = None
        mock_update_doc_length.return_value = None

        # Gọi hàm chính trong run.py
        run.main()

        # Kiểm tra các hàm được gọi đúng
        self.assertTrue(mock_extract_sitemaps.called)
        self.assertTrue(mock_extract_urls_from_sitemap.called)
        mock_insert_document.assert_called_with('http://example.com/page1', 'Content 1', 'Title 1')
        self.assertTrue(mock_get_unvisited_documents.called)
        self.assertTrue(mock_count_documents.called)
        self.assertTrue(mock_upsert_index_batch.called)
        self.assertTrue(mock_update_df.called)
        self.assertTrue(mock_update_doc_length.called)

    @patch('common.extract_sitemaps')
    @patch('common.extract_urls_from_sitemap')
    @patch('vietnamnet_crawler.crawler.is_url_visited')
    def test_crawl_no_new_urls(
        self,
        mock_is_url_visited,
        mock_extract_urls_from_sitemap,
        mock_extract_sitemaps
    ):
        # Mock dữ liệu: không có URL mới để crawl
        mock_extract_sitemaps.return_value = [
            f'http://example.com/sitemap{i}.xml' for i in range(6)
        ]
        mock_extract_urls_from_sitemap.return_value = ['http://example.com/page1']
        mock_is_url_visited.return_value = True  # URL đã được visited

        # Gọi crawl_and_insert
        crawl_and_insert()

        # Kiểm tra không gọi thêm hàm insert_document vì không có URL mới
        self.assertTrue(mock_extract_sitemaps.called)
        self.assertTrue(mock_extract_urls_from_sitemap.called)
        self.assertTrue(mock_is_url_visited.called)

    @patch('common.extract_sitemaps')
    @patch('common.extract_urls_from_sitemap')
    @patch('vietnamnet_crawler.craw_helper.extract_text_from_url')
    @patch('vietnamnet_crawler.crawler.insert_document')
    @patch('vietnamnet_crawler.crawler.is_url_visited')  # Thêm mock cho is_url_visited
    def test_crawl_error(
        self,
        mock_is_url_visited,
        mock_insert_document,
        mock_extract_text_from_url,
        mock_extract_urls_from_sitemap,
        mock_extract_sitemaps
    ):
        # Mock dữ liệu: crawl thất bại
        mock_extract_sitemaps.return_value = [
            f'http://example.com/sitemap{i}.xml' for i in range(6)
        ]
        mock_extract_urls_from_sitemap.return_value = ['http://example.com/page1']
        mock_is_url_visited.return_value = False  # URL chưa được visited
        mock_extract_text_from_url.return_value = None  # Crawl lỗi

        # Gọi crawl_and_insert
        crawl_and_insert()

        # Kiểm tra không gọi insert_document vì crawl thất bại
        self.assertTrue(mock_extract_sitemaps.called)
        self.assertTrue(mock_extract_urls_from_sitemap.called)
        self.assertTrue(mock_extract_text_from_url.called)
        self.assertFalse(mock_insert_document.called)

    @patch('storage_pg.get_unvisited_documents')
    @patch('storage_pg.count_documents')
    @patch('storage_pg.get_df_batch')
    def test_index_error(
        self,
        mock_get_df_batch,
        mock_count_documents,
        mock_get_unvisited_documents
    ):
        # Mock dữ liệu: lỗi khi lấy dữ liệu từ DB
        mock_get_unvisited_documents.return_value = [(1, 'http://example.com/page1', 'Title 1', 'Content 1')]
        mock_count_documents.return_value = 1
        mock_get_df_batch.side_effect = Exception("Database error")

        # Gọi index_documents và kiểm tra lỗi
        with self.assertRaises(Exception) as context:
            index_documents()
        self.assertTrue("Database error" in str(context.exception))

if __name__ == '__main__':
    unittest.main()