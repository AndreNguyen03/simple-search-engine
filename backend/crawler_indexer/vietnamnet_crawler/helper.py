import requests
from bs4 import BeautifulSoup



def extract_text_from_url(url: str, session: requests.Session) -> str:
    try:
        res = session.get(url, timeout=5)
        if res.status_code != 200:
            return ''

        soup = BeautifulSoup(res.text, 'html.parser')
        h1 = soup.find('h1', class_='content-detail-title')
        if h1 is None:
            return ''

        content_div = soup.find('div', id='maincontent', class_='maincontent main-content')
        if not content_div:
            return ''

        paragraphs = content_div.find_all('p')
        chunks = [h1.get_text(strip=True)]

        for p in paragraphs[:4]:  # Giới hạn số đoạn đầu tiên
            chunks.append(p.get_text(strip=True))

        return '\n'.join(chunks)
    except Exception as e:
        print(f"[Helper] ❌ Lỗi khi crawl {url}: {e}")
        return ''