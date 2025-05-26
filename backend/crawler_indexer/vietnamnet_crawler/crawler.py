from . import craw_helper
from storage_pg import insert_document, get_conn
import common
import requests
from concurrent.futures import ThreadPoolExecutor

def crawl_and_insert():
    sitemap_url = 'http://vietnamnet.vn/sitemap.xml'
    print("[Crawler] Bắt đầu lấy danh sách sitemap từ:", sitemap_url)
    sitemaps = common.extract_sitemaps(sitemap_url)
    print(f"[Crawler] Lấy được {len(sitemaps)} sitemap.")

    for sitemap in sitemaps[4:5]:
        print(f"[Crawler] Xử lý sitemap: {sitemap}")
        urls = common.extract_urls_from_sitemap(sitemap)
        print(f"[Crawler] Lấy được {len(urls)} URL từ sitemap.")
        urls_to_process = [url for url in urls if not is_url_visited(url)]
        print(f"[Crawler] 📌 Sẽ xử lý {len(urls_to_process)} URL mới.")

        with requests.Session() as session:
            with ThreadPoolExecutor(max_workers=10) as executor:
                for i, url in enumerate(urls_to_process, start=1):
                    executor.submit(process_url, i, url, session)

def process_url(index: int, url: str, session: requests.Session):
    print(f"[Crawler] 🚀 {index}. Đang crawl: {url}")
    title, description = craw_helper.extract_text_from_url(url, session)
    if (description and title):
        insert_document(url, description, title)
        print(f"[Crawler] ✅ Đã lưu URL: {url}")
    else:
        print(f"[Crawler] ⚠️ Không lấy được nội dung từ URL: {url}")

def is_url_visited(url: str) -> bool:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM documents WHERE url = %s', (url,))
    result = cursor.fetchone() is not None
    conn.close()
    return result

