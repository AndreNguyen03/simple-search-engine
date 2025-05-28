import os

PG_HOST = os.getenv('PG_HOST', 'localhost')
PG_PORT = int(os.getenv('PG_PORT', 5432))
PG_USER = os.getenv('PG_USER', 'admin')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'securepassword')
PG_DB = os.getenv('PG_DB', 'myapp')

print(f"Using PostgreSQL config: {PG_HOST}:{PG_PORT}, DB: {PG_DB}, User: {PG_USER}")
