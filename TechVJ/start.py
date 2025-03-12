# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import asyncio 
import random
import time
import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from database.db import db
from TechVJ.strings import HELP_TXT
from datetime import datetime
from asyncio import Semaphore

class batch_temp(object):
    IS_BATCH = {}

semaphore = Semaphore(5)  # Controls concurrent downloads

async def status_handler(status_file, message, action):
    while not os.path.exists(status_file):
        await asyncio.sleep(3)
    
    while os.path.exists(status_file):
        with open(status_file, "r") as f:
            txt = f.read()
        try:
            await message.edit_text(f"**{action}:** **{txt}**")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)

def progress(current, total, message, _type):
    with open(f'{message.id}{_type}status.txt', "w") as f:
        f.write(f"{current * 100 / total:.1f}%")

@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
    
    buttons = [
        [InlineKeyboardButton("❣️ Developer", url="https://t.me/kingvj01")],
        [
            InlineKeyboardButton('🔍 Support Group', url='https://t.me/vj_bot_disscussion'),
            InlineKeyboardButton('🤖 Update Channel', url='https://t.me/vj_botz')
        ]
    ]
    
    await message.reply_text(
        text=f"<b>👋 Hi {message.from_user.mention}, I'm Save Restricted Content Bot</b>",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_message(filters.command(["help"]))
async def send_help(client: Client, message: Message):
    await message.reply_text(HELP_TXT)

@Client.on_message(filters.command(["cancel"]))
async def send_cancel(client: Client, message: Message):
    batch_temp.IS_BATCH[message.from_user.id] = True
    await message.reply_text("**Batch Successfully Cancelled.**")

async def handle_large_file(client, acc, message, file_path, msg):
    chunk_size = 10 * 1024 * 1024  # 10MB chunks
    file_size = os.path.getsize(file_path)
    
    with open(file_path, 'rb') as f:
        part_num = 1
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            await client.send_document(
                message.chat.id,
                chunk,
                file_name=f"{os.path.basename(file_path)}.part{part_num}",
                reply_to_message_id=message.id
            )
            part_num += 1
            await asyncio.sleep(2)  # Reduce flood risk

async def download_with_retry(acc, msg, message):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            return await acc.download_media(msg, progress=progress, progress_args=[message, "down"])
        except FloodWait as e:
            wait = e.value + random.randint(5, 15)
            await asyncio.sleep(wait)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2)
    return None

@Client.on_message(filters.text & filters.private)
async def save(client: Client, message: Message):
    if "https://t.me/" not in message.text:
        return
    
    user_id = message.from_user.id
    batch_temp.IS_BATCH[user_id] = False
    
    async with semaphore:
        try:
            # Rest of your existing message processing logic
            # ... [Keep your existing URL parsing and message ID logic]
            
            # Modified download section
            smsg = await message.reply('**Downloading...**')
            file_path = await download_with_retry(acc, msg, message)
            
            if os.path.getsize(file_path) > 100 * 1024 * 1024:  # 100MB
                await handle_large_file(client, acc, message, file_path, msg)
            else:
                # Existing upload logic
                await client.send_document(
                    message.chat.id,
                    file_path,
                    reply_to_message_id=message.id,
                    progress=progress,
                    progress_args=[message, "up"]
                )
            
            # Cleanup
            if os.path.exists(file_path):
                os.remove(file_path)
            
        except Exception as e:
            await message.reply_text(f"Error: {str(e)}")
        finally:
            batch_temp.IS_BATCH[user_id] = True
