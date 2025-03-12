import os

# Bot token @Botfather
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7702562393:AAF8xIGuvLgK39IuyqdvIpVROwX9zapzfOA")

# Your API ID from my.telegram.org
API_ID = int(os.environ.get("API_ID", "27997082"))

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "6f3a423cc9f69c28ed9f99a42776bcf0")

# Your Owner / Admin Id For Broadcast 
ADMINS = int(os.environ.get("ADMINS", "1874350266"))

# Your Mongodb Database Url
DB_URI = os.environ.get("DB_URI", "")
DB_NAME = os.environ.get("DB_NAME", "vjsavecontentbot")

# Error Message Settings
ERROR_MESSAGE = bool(os.environ.get('ERROR_MESSAGE', True))

# New Rate Limit Configs
MAX_CONCURRENT_TASKS = 3  # Max parallel downloads per user
REQUEST_DELAY = 2  # Seconds between requests
BROADCAST_DELAY = 1.5  # Seconds between broadcast messages
