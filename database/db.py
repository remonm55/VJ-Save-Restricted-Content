import motor.motor_asyncio
from config import DB_NAME, DB_URI

class Database:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
        self.db = self.client[DB_NAME]
        self.col = self.db.users

    # Keep all your existing methods below unchanged
    # ... [Rest of your original db.py code here]

db = Database()
