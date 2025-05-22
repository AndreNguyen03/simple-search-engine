import requests
from bs4 import BeautifulSoup
from typing import Optional, Tuple

def extract_text_from_url(url: str, session: requests.Session) -> Optional[Tuple[str, str]]:
    try:
        res = session.get(url, timeout=5)
        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Lấy tiêu đề bài viết
        h1 = soup.find('h1', class_='content-detail-title')
        title = h1.get_text(strip=True) if h1 else ''
        # Lấy phần nội dung chính
        content_div = soup.find('div', id='maincontent', class_='maincontent main-content')
        if not content_div:
            return None

        paragraphs = content_div.find_all('p')
        description_chunks = []

        for p in paragraphs[:4]:  # Giới hạn số đoạn mô tả
            text = p.get_text(strip=True)
            if text:
                description_chunks.append(text)

        description = '\n'.join(description_chunks)

        return title, description

    except Exception as e:
        print(f"[Helper] ❌ Lỗi khi crawl {url}: {e}")
        return None
