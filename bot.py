from pyrogram import Client
from pyrogram.errors import FloodWait
from config import API_ID, API_HASH, BOT_TOKEN
import asyncio
import time
import os

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="techvj_session",  # Changed session name
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="TechVJ"),
            workers=2,  # Reduced workers
            sleep_threshold=60,
            in_memory=False  # Enable session persistence
        )

    async def safe_start(self):
        attempts = 0
        max_attempts = 3
        while attempts < max_attempts:
            try:
                await self.start()
                print('Bot Started Successfully')
                await self.idle()
            except FloodWait as e:
                wait = e.value + 30
                print(f'FloodWait: Sleeping {wait} seconds')
                time.sleep(wait)
                attempts += 1
            except Exception as e:
                print(f'Critical Error: {e}')
                break
            finally:
                await self.stop()
        print('Failed to start after multiple attempts')

if __name__ == "__main__":
    bot = Bot()
    asyncio.run(bot.safe_start())
