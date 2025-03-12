import os
import asyncio
import logging
import psutil
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import *
from database.db import db

logger = logging.getLogger(__name__)

class TurboEngine:
    active_tasks = {}
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    @staticmethod
    async def memory_safe():
        mem = psutil.virtual_memory()
        return (mem.available / 1024 / 1024) > MEMORY_LIMIT

async def turbo_download(client, acc, msg, message):
    try:
        file = await acc.download_media(
            msg,
            file_name=f"turbo_{message.id}.temp",
            block=False,
            chunk_size=CHUNK_SIZE
        )
        return file
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        raise

async def turbo_upload(client, message, file):
    try:
        await client.send_document(
            message.chat.id,
            file,
            force_document=True,
            progress=progress_handler,
            progress_args=(message.id, "up")
        )
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise

async def progress_handler(current, total, message_id, direction):
    progress = f"{current * 100 / total:.1f}%"
    try:
        with open(f"{message_id}_{direction}.progress", "w") as f:
            f.write(progress)
    except:
        pass

@Client.on_message(filters.command(["start", "help", "cancel"]))
async def command_handler(client: Client, message: Message):
    await message.reply("⚡ Turbo Mode Active ⚡")

@Client.on_message(filters.text & filters.private)
async def turbo_handler(client: Client, message: Message):
    user_id = message.from_user.id
    
    if not await TurboEngine.memory_safe():
        await message.reply("⚠️ Server resources busy, try again later")
        return

    async with TurboEngine.semaphore:
        try:
            # Get user session
            user_data = await db.get_session(user_id)
            if not user_data:
                await message.reply("🔑 Please /login first")
                return

            # Process message
            async with Client(
                "turbo_client",
                session_string=user_data,
                api_id=API_ID,
                api_hash=API_HASH,
                config_file="telegram.ini"
            ) as acc:
                
                # Download
                file = await turbo_download(client, acc, msg, message)
                await asyncio.sleep(REQUEST_DELAY)
                
                # Upload
                await turbo_upload(client, message, file)

        except Exception as e:
            logger.error(f"Turbo failed: {str(e)}")
            await message.reply(f"❌ Error: {str(e)}")
        finally:
            # Cleanup
            for f in [file, 
                     f"{message.id}_up.progress",
                     f"{message.id}_down.progress"]:
                try:
                    if os.path.exists(f):
                        os.remove(f)
                except:
                    pass
