# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import os

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="techvj_login",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="TechVJ"),
            workers=int(os.environ.get("WORKERS", 100)),
            sleep_threshold=int(os.environ.get("SLEEP_THRESHOLD", 30)),
            max_concurrent_transmissions=int(os.environ.get("MAX_CONCURRENT", 10)),
            in_memory=True
        )

    async def start(self):
        await super().start()
        print('Bot Started Powered By @VJ_Botz')

    async def stop(self, *args):
        await super().stop()
        print('Bot Stopped Bye')

if __name__ == "__main__":
    Bot().run()
