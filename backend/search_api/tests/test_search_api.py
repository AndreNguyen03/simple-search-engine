import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app, SearchRequest
from typing import List
import time

class TestSearchAPI(unittest.TestCase):
    def setUp(self):
        # Khởi tạo TestClient để gọi API
        self.client = TestClient(app)
    
    @patch('search.search')
    def test_search_valid_query(self, mock_search):
        # Mock kết quả từ hàm search.search
        mock_results = [
            {
                'doc_id': 1,
                'url': 'http://example.com',
                'title': 'Example',
                'snippet': 'This is a test document...',
                'score': 0.95
            }
        ]
        mock_total = 1
        mock_time = 0.123
        mock_search.return_value = (mock_results, mock_total, mock_time)

        # Gửi yêu cầu POST tới endpoint /search
        request = SearchRequest(query="test query", page=1, limit=20)
        response = self.client.post("/api/search", json=request.model_dump())

        # Kiểm tra status code và nội dung trả về
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["query"], "test query")
        self.assertEqual(result["results"], mock_results)
        self.assertEqual(result["total"], mock_total)
        self.assertEqual(result["page"], 1)
        self.assertEqual(result["limit"], 20)
        self.assertAlmostEqual(result["time"], mock_time, places=3)

    @patch('search.search')
    def test_search_empty_query(self, mock_search):
        # Mock trường hợp truy vấn không có kết quả
        mock_search.return_value = ([], 0, 0.05)

        # Gửi yêu cầu với truy vấn rỗng
        request = SearchRequest(query="", page=1, limit=20)
        response = self.client.post("/api/search", json=request.model_dump())

        # Kiểm tra kết quả
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["query"], "")
        self.assertEqual(result["results"], [])
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["page"], 1)
        self.assertEqual(result["limit"], 20)
        self.assertAlmostEqual(result["time"], 0.05, places=3)

    @patch('search.search')
    def test_search_pagination(self, mock_search):
        # Mock kết quả với nhiều document để kiểm tra phân trang
        mock_results = [
            {
                'doc_id': i,
                'url': f'http://example.com/{i}',
                'title': f'Example {i}',
                'snippet': f'This is document {i}...',
                'score': 0.9 - i * 0.1
            } for i in range(15)  # 15 kết quả
        ]
        mock_total = 15
        mock_time = 0.2
        mock_search.return_value = (mock_results[10:15], mock_total, mock_time)  # Page 2, limit 5

        # Gửi yêu cầu với page=2, limit=5
        request = SearchRequest(query="test query", page=2, limit=5)
        response = self.client.post("/api/search", json=request.model_dump())

        # Kiểm tra kết quả
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(len(result["results"]), 5)  # Chỉ trả về 5 kết quả
        self.assertEqual(result["results"][0]["doc_id"], 10)  # Kết quả từ doc_id 10
        self.assertEqual(result["total"], mock_total)
        self.assertEqual(result["page"], 2)
        self.assertEqual(result["limit"], 5)
        self.assertAlmostEqual(result["time"], mock_time, places=3)

    @patch('search.search')
    def test_search_error(self, mock_search):
        # Mock trường hợp search ném ra exception
        mock_search.side_effect = Exception("Database connection error")

        # Gửi yêu cầu
        request = SearchRequest(query="test query", page=1, limit=20)
        response = self.client.post("/api/search", json=request.model_dump())

        # Kiểm tra status code và lỗi
        self.assertEqual(response.status_code, 500)
        self.assertIn("detail", response.json())
        self.assertIn("Database connection error", response.json()["detail"])

if __name__ == '__main__':
    unittest.main()