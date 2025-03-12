from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from database.db import db
from pyrogram import Client, filters
from config import ADMINS
import asyncio
import datetime
import time
from typing import Tuple

BROADCAST_LIMIT = 20  # Messages per minute
BROADCAST_DELAY = 60 / BROADCAST_LIMIT

async def broadcast_messages(user_id: int, message) -> Tuple[bool, str]:
    try:
        await message.copy(chat_id=user_id)
        await asyncio.sleep(BROADCAST_DELAY)  # Rate limiting
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value + 1)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(user_id)
        return False, "Deleted"
    except UserIsBlocked:
        await db.delete_user(user_id)
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(user_id)
        return False, "Error"
    except Exception as e:
        logger.error(f"Broadcast error for {user_id}: {e}")
        return False, "Error"

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_handler(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    
    if not b_msg:
        return await message.reply_text("Please reply to a message to broadcast")
        
    status_msg = await message.reply_text("Broadcasting your messages...")
    
    start_time = time.time()
    total_users = await db.total_users_count()
    stats = {
        'done': 0,
        'success': 0,
        'blocked': 0,
        'deleted': 0,
        'failed': 0
    }

    async for user in users:
        if 'id' not in user:
            stats['failed'] += 1
            continue
            
        result, status = await broadcast_messages(user['id'], b_msg)
        
        if result:
            stats['success'] += 1
        else:
            if status == "Blocked":
                stats['blocked'] += 1
            elif status == "Deleted":
                stats['deleted'] += 1
            else:
                stats['failed'] += 1
                
        stats['done'] += 1
        
        if stats['done'] % 20 == 0:
            await status_msg.edit(
                f"Broadcast progress:\n\n"
                f"Total Users: {total_users}\n"
                f"Completed: {stats['done']}/{total_users}\n"
                f"Success: {stats['success']}\n"
                f"Blocked: {stats['blocked']}\n"
                f"Deleted: {stats['deleted']}\n"
                f"Failed: {stats['failed']}"
            )

    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await status_msg.edit(
        f"Broadcast completed in {time_taken}:\n\n"
        f"Total Users: {total_users}\n"
        f"Success: {stats['success']}\n"
        f"Blocked: {stats['blocked']}\n"
        f"Deleted: {stats['deleted']}\n"
        f"Failed: {stats['failed']}"
    )
