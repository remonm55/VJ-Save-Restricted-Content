import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
ADMINS = int(os.environ.get("ADMINS", 0))
DB_URI = os.environ.get("DB_URI", "")
DB_NAME = os.environ.get("DB_NAME", "turbo_bot")

# Turbo Performance Settings
MAX_CONCURRENT = 12
CHUNK_SIZE = 50 * 1024 * 1024  # 50MB chunks
REQUEST_DELAY = 0.5  # 500ms
MAX_FILE_SIZE = 2048  # 2GB in MB
MEMORY_LIMIT = 12288  # 12GB RAM buffer
LOG_LEVEL = "INFO"
