import motor.motor_asyncio
from config import DB_NAME, DB_URI
from typing import Optional, Dict, Any

class Database:
    def __init__(self, uri: str, database_name: str):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(
            uri,
            maxPoolSize=20,
            minPoolSize=5,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000
        )
        self.db = self._client[database_name]
        self.col = self.db.users

    async def close(self):
        await self._client.close()

    def new_user(self, id: int, name: str) -> Dict[str, Any]:
        return {
            'id': id,
            'name': name,
            'session': None,
            'last_active': None
        }

    async def add_user(self, id: int, name: str) -> None:
        user = self.new_user(id, name)
        await self.col.insert_one(user)

    async def is_user_exist(self, id: int) -> bool:
        return bool(await self.col.find_one({'id': id}))

    async def total_users_count(self) -> int:
        return await self.col.count_documents({})

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id: int) -> None:
        await self.col.delete_many({'id': user_id})

    async def set_session(self, id: int, session: Optional[str]) -> None:
        await self.col.update_one(
            {'id': id},
            {'$set': {'session': session, 'last_active': datetime.utcnow()}}
        )

    async def get_session(self, id: int) -> Optional[str]:
        user = await self.col.find_one({'id': id})
        return user.get('session') if user else None

db = Database(DB_URI, DB_NAME)
