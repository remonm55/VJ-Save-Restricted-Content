import motor.motor_asyncio
from config import DB_NAME, DB_URI

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(
            uri,
            maxPoolSize=10,
            minPoolSize=2,
            connectTimeoutMS=30000,
            serverSelectionTimeoutMS=30000
        )
        self.db = self._client[database_name]
        self.col = self.db.users

    # ... [Keep all original methods unchanged] ...

db = Database(DB_URI, DB_NAME)
