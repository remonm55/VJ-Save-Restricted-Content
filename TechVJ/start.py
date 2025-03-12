# ... [Keep the original header comments] ...

import os
import asyncio 
import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from config import API_ID, API_HASH, ERROR_MESSAGE, MAX_CONCURRENT_TASKS, REQUEST_DELAY
from database.db import db

class batch_temp(object):
    IS_BATCH = {}

async def downstatus(client, statusfile, message, chat):
    while True:
        if os.path.exists(statusfile):
            break
        await asyncio.sleep(3)
      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            await client.edit_message_text(chat, message.id, f"**Downloaded:** **{txt}**")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)

async def upstatus(client, statusfile, message, chat):
    while True:
        if os.path.exists(statusfile):
            break
        await asyncio.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            await client.edit_message_text(chat, message.id, f"**Uploaded:** **{txt}**")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)

def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")

@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):
    # ... [Keep original start command unchanged] ...

@Client.on_message(filters.command(["help"]))
async def send_help(client: Client, message: Message):
    # ... [Keep original help command unchanged] ...

@Client.on_message(filters.command(["cancel"]))
async def send_cancel(client: Client, message: Message):
    batch_temp.IS_BATCH[message.from_user.id] = True
    await client.send_message(message.chat.id, "**Batch Successfully Cancelled.**")

@Client.on_message(filters.text & filters.private)
async def save(client: Client, message: Message):
    if "https://t.me/" not in message.text:
        return
    
    user_id = message.from_user.id
    if batch_temp.IS_BATCH.get(user_id) == False:
        return await message.reply_text("**Another task is in progress. Use /cancel to abort.**")
    
    batch_temp.IS_BATCH[user_id] = False
    sem = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
    
    try:
        datas = message.text.split("/")
        temp = datas[-1].replace("?single","").split("-")
        fromID = int(temp[0].strip())
        toID = int(temp[1].strip()) if len(temp) > 1 else fromID
        
        async def process_msg(msgid):
            async with sem:
                if batch_temp.IS_BATCH.get(user_id):
                    return
                
                await asyncio.sleep(REQUEST_DELAY)  # Rate limiting
                
                user_data = await db.get_session(user_id)
                if not user_data:
                    await message.reply("**Please /login first.**")
                    batch_temp.IS_BATCH[user_id] = True
                    return
                
                try:
                    async with Client("saverestricted", session_string=user_data, 
                                    api_hash=API_HASH, api_id=API_ID) as acc:
                        # ... [Keep original media handling logic] ...
                        # Add proper cleanup in finally blocks
                except Exception as e:
                    if ERROR_MESSAGE:
                        await client.send_message(user_id, f"Error: {str(e)}")
        
        tasks = []
        for msgid in range(fromID, toID+1):
            if batch_temp.IS_BATCH.get(user_id):
                break
            tasks.append(process_msg(msgid))
            if len(tasks) >= MAX_CONCURRENT_TASKS * 2:
                await asyncio.gather(*tasks)
                tasks = []
        
        if tasks:
            await asyncio.gather(*tasks)
            
    except Exception as e:
        await message.reply(f"Error processing request: {str(e)}")
    finally:
        batch_temp.IS_BATCH[user_id] = True
        # Add any necessary cleanup

# ... [Keep remaining helper functions but add cleanup] ...
