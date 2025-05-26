
# 🔍 Search Engine Project

Một hệ thống tìm kiếm bao gồm:
- **Crawler/Indexer**: Thu thập và lập chỉ mục dữ liệu từ Vietnamnet.
- **Search API**: API cung cấp khả năng tìm kiếm dữ liệu.
- **Frontend**: Giao diện người dùng để nhập truy vấn tìm kiếm.
- **PostgreSQL**: Cơ sở dữ liệu lưu trữ dữ liệu đã thu thập.

## 📦 Cấu trúc thư mục

```
.
├── backend/
│   ├── crawler_indexer/      # Crawler và Indexer
│   └── search_api/           # FastAPI Search API
├── frontend/                 # Ứng dụng frontend (Vite + Bun/Node)
├── docker-compose.yml        # Định nghĩa các service Docker
└── README.md
```

## 🚀 Khởi chạy dự án với Docker Compose

> Yêu cầu: Docker & Docker Compose đã được cài đặt sẵn.

Chạy tất cả các service với:

```bash
docker-compose up --build
```

Quá trình này sẽ:
- Tải image PostgreSQL (nếu chưa có).
- Build từng Dockerfile cho `crawler_indexer`, `search_api` và `frontend`.
- Khởi chạy hệ thống mạng nội bộ để các service kết nối với nhau.

## 🔗 Truy cập các thành phần

| Thành phần       | Địa chỉ                     | Mô tả                             |
|------------------|-----------------------------|-----------------------------------|
| Frontend         | http://localhost:5173       | Giao diện người dùng              |
| Search API       | http://localhost:8000/docs  | Swagger UI của Search API         |
| PostgreSQL       | localhost:5432              | DB PostgreSQL (user: `myuser`, password: `mypassword`) |

## ⚙️ Môi trường PostgreSQL

```env
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydb
```

Volume dữ liệu sẽ được lưu trữ tại: `pgdata:/var/lib/postgresql/data`

## 📂 Thông tin các service trong `docker-compose.yml`

### 1. `postgres`
- Image: `postgres:15`
- Cổng: `5432`
- Dữ liệu lưu trong volume: `pgdata`

### 2. `crawler_indexer`
- Đọc dữ liệu từ Vietnamnet và lập chỉ mục
- Mount source code từ: `./backend/crawler_indexer:/app`
- Chạy kèm sau khi PostgreSQL sẵn sàng

### 3. `search_api`
- Dựng bằng **FastAPI**
- Expose cổng `8000`
- Mount source code từ: `./backend/search_api:/app`
- Có tài liệu API tại `/docs`

### 4. `frontend`
- Xây dựng từ Dockerfile Vite
- Chạy ở chế độ preview tại cổng `5173`
- Phụ thuộc vào `search_api`

## 🧹 Dọn dẹp hệ thống

Dừng và xóa toàn bộ container, mạng và volumes:

```bash
docker-compose down -v
```

---

## ⚡️ Chạy thủ công từng service (Không dùng Docker)

### 1. Cài PostgreSQL thủ công
- Tạo user `myuser` và database `mydb` với mật khẩu `mypassword`
- Mở cổng `5432` nếu cần

### 2. Chạy `crawler_indexer`
```bash
cd backend/crawler_indexer
python -m venv venv
venv\Scripts\activate      # Hoặc `source venv/bin/activate` trên Linux/Mac
pip install -r requirements.txt
python run.py
```

### 3. Chạy `search_api`
```bash
cd backend/search_api
python -m venv venv
venv\Scripts\activate      # Hoặc `source venv/bin/activate` trên Linux/Mac
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Chạy frontend (Vite)
```bash
cd frontend
bun install                 # Hoặc `npm install`
bun run dev                # Hoặc `npm run dev`
```

Mặc định frontend sẽ chạy tại: http://localhost:5173

---

## 🛠 Troubleshooting

- Nếu không thấy dữ liệu, kiểm tra log của `crawler_indexer`:
  ```bash
  docker logs crawler_indexer
  ```
- Nếu port `5173`, `8000` hoặc `5432` đã bị chiếm, chỉnh sửa `docker-compose.yml` phần `ports`.

---

## 📄 Giấy phép

MIT License.
