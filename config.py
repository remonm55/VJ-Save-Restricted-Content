import os

# Bot configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
ADMINS = int(os.environ.get("ADMINS", 0))

# Database configuration
DB_URI = os.environ.get("DB_URI", "")
DB_NAME = os.environ.get("DB_NAME", "vjsavecontentbot")

# Performance settings
MAX_CONCURRENT_TASKS = int(os.environ.get("MAX_CONCURRENT_TASKS", 10))
DOWNLOAD_TIMEOUT = int(os.environ.get("DOWNLOAD_TIMEOUT", 300))
UPLOAD_TIMEOUT = int(os.environ.get("UPLOAD_TIMEOUT", 300))

# Error handling
ERROR_MESSAGE = bool(os.environ.get('ERROR_MESSAGE', True))
ERROR_RETRY_COUNT = int(os.environ.get('ERROR_RETRY_COUNT', 3))

# Rate limiting
BROADCAST_LIMIT = int(os.environ.get("BROADCAST_LIMIT", 20))  # Messages per minute
REQUEST_LIMIT = int(os.environ.get("REQUEST_LIMIT", 5))  # Requests per second
