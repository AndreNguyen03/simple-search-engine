import sqlite3
import storage
from config import DB_PATH

def list_tables():
    conn = storage.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return [table[0] for table in tables]

print(list_tables())