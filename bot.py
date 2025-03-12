from pyrogram import Client, idle
from pyrogram.errors import FloodWait
from config import API_ID, API_HASH, BOT_TOKEN
import asyncio
import time

class Bot(Client):
    def __init__(self):
        super().__init__(
            "techvj_session",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="TechVJ"),
            workers=2,
            sleep_threshold=30
        )

    async def safe_start(self):
        attempts = 0
        max_attempts = 3
        while attempts < max_attempts:
            try:
                await self.start()
                print('Bot Started Successfully')
                await idle()  # Corrected idle usage
                return True
            except FloodWait as e:
                wait = e.value + 10
                print(f'⏳ FloodWait: Sleeping {wait} seconds')
                time.sleep(wait)
                attempts += 1
            except Exception as e:
                print(f'🚨 Critical Error: {e}')
                break
            finally:
                if self.is_initialized:
                    await self.stop()
                    print('Bot Stopped Cleanly')
        return False

if __name__ == "__main__":
    bot = Bot()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.safe_start())
    except KeyboardInterrupt:
        print('\n🚫 Manual Interruption - Shutting Down')
    finally:
        loop.close()
