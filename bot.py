from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import asyncio
import time

class Bot(Client):
    def __init__(self):
        super().__init__(
            "techvj_login",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="TechVJ"),
            workers=4,  # Reduced workers
            sleep_threshold=30,
            in_memory=True
        )

    async def start(self):
        retries = 0
        max_retries = 5
        while retries < max_retries:
            try:
                await super().start()
                print('Bot Started Powered By @VJ_Botz')
                return
            except FloodWait as e:
                wait = e.value + 10
                print(f'FloodWait: Sleeping {wait} seconds')
                time.sleep(wait)
                retries += 1
            except Exception as e:
                print(f'Start failed: {e}')
                break
        print('Bot failed to start')

    async def stop(self, *args):
        await super().stop()
        print('Bot Stopped Bye')

if __name__ == "__main__":
    asyncio.run(Bot().start())
