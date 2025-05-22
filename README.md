# simple-search-engine

# VietnamNet SimepleSearchEngine 

## Mô tả chung

Dự án này bao gồm 2 phần chính:  
- **Backend:** Crawler, indexer và API tìm kiếm sử dụng FastAPI, Python  
- **Frontend:** Giao diện web tìm kiếm React + TailwindCSS + Vite  

---

## Cấu trúc thư mục

```
backend/
├── crawler_indexer/          # Crawler và indexer dữ liệu
│   ├── indexer/
│   └── vietnamnet_crawler/
├── data/                     # Database lưu trữ (SQLite)
├── search.api/               # API tìm kiếm FastAPI
├── requirements.txt          # Thư viện backend
├── config.py                 # Cấu hình chung
├── helper.py                 # Hàm hỗ trợ
├── stopwords.py             # Bộ lọc stopwords
├── storage.py               # Xử lý lưu trữ và truy xuất dữ liệu
└── vietnamese-stopwords-dash.txt  # File stopwords

frontend/
├── public/                   # File tĩnh
├── src/                      # Source code React
├── package.json              # Quản lý thư viện frontend
├── tailwind.config.ts        # Cấu hình TailwindCSS
├── tsconfig.json             # Cấu hình TypeScript
├── vite.config.ts            # Cấu hình Vite
└── ...                       # Các file cấu hình khác
```

---

## Hướng dẫn cài đặt và chạy

### Backend

1. Tạo môi trường ảo (khuyến khích):

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

2. Cài đặt thư viện:

```bash
pip install -r requirements.txt
```

3. Chạy crawler + indexer để thu thập dữ liệu:

```bash
python -m crawler_indexer.run
```

4. Chạy API server:

```bash
uvicorn search_api.main:app --reload
```


---

### Frontend

1. Cài đặt các package:

```bash
npm install
```

2. Chạy frontend:

```bash
npm run dev
```

---

## Công nghệ sử dụng

- Python, FastAPI, SQLite cho backend và API  
- React, TypeScript, TailwindCSS, Vite cho frontend  
- Crawler tự động lấy dữ liệu từ VietnamNet để lập chỉ mục tìm kiếm  
- Inverted Index và TF-IDF cho thuật toán tìm kiếm

---

## Ghi chú

- Đảm bảo chạy crawler trước để có dữ liệu cho API tìm kiếm  
- Cấu hình API backend và frontend có thể điều chỉnh trong file config riêng  
