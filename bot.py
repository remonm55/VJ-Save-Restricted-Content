from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Bot(Client):
    def __init__(self):
        super().__init__(
            "turbo_saver",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="TechVJ"),
            workers=16,
            sleep_threshold=5,
            max_concurrent_transmissions=12,
            workdir="./sessions",
            config_file="telegram.ini"
        )

    async def start(self):
        await super().start()
        logger.info('⚡ TURBO MODE ACTIVATED ⚡')
        
    async def stop(self, *args):
        await super().stop()
        logger.info('Turbo Engine Stopped')

if __name__ == "__main__":
    Bot().run()
