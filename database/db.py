import motor.motor_asyncio
from config import DB_NAME, DB_URI

class Database:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
        self.db = self.client[DB_NAME]
        self.col = self.db.users

    # Fixed method name to match exactly what's being called
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)

    # Keep all original methods below unchanged
    def new_user(self, id, name):
        return dict(
            id=id,
            name=name,
            session=None
        )
    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
    
    async def total_users_count(self):
        return await self.col.count_documents({})

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def set_session(self, id, session):
        await self.col.update_one(
            {'id': int(id)},
            {'$set': {'session': session}}
        )

    async def get_session(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('session') if user else None

# Initialize database instance
db = Database()
