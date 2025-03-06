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
# Warning - Give Db uri in deploy server environment variable, don't give in repo.
DB_URI = os.environ.get("DB_URI", "") # Warning - Give Db uri in deploy server environment variable, don't give in repo.
DB_NAME = os.environ.get("DB_NAME", "vjsavecontentbot")

# If You Want Error Message In Your Personal Message Then Turn It True Else If You Don't Want Then Flase
ERROR_MESSAGE = bool(os.environ.get('ERROR_MESSAGE', True))
