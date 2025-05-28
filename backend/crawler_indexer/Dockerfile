FROM python:3.10-slim

WORKDIR /app

# Copy requirements để tận dụng cache
COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

RUN rm -rf .venv

CMD ["python", "run.py"]
