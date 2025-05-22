import os

# Đặt DB_PATH ra ngoài project để dễ chia sẻ giữa các module
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'search.db')

# Đảm bảo folder data tồn tại
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)