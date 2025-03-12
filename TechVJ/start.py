# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import asyncio 
import random
import time
import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.types import Message  # Added missing import
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

# Rest of the file remains the same...
