import motor.motor_asyncio
from config import DB_NAME, DB_URI
from motor.core import AgnosticClient

class Database:
    _client: AgnosticClient = None
    
    def __init__(self):
        self.db = self.client[DB_NAME]
        self.col = self.db.users

    @property
    def client(self):
        if self._client is None:
            self._client = motor.motor_asyncio.AsyncIOMotorClient(
                DB_URI,
                maxPoolSize=100,
                minPoolSize=10,
                connectTimeoutMS=30000,
                socketTimeoutMS=30000
            )
        return self._client
    
    # Keep all existing methods unchanged below
    # ... [Rest of your existing methods]

db = Database()
