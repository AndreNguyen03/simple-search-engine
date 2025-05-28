FROM python:3.10-slim

# Cài đặt thư viện hệ thống cần thiết
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục làm việc
WORKDIR /app

# Copy requirements trước để tận dụng cache Docker layer
COPY requirements.txt .

# Cài dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy phần còn lại của source code
COPY . .

RUN rm -rf .venv


# Mở cổng API
EXPOSE 8000

# Lệnh khởi động ứng dụng
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
