import traceback
from pyrogram.types import Message
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from config import API_ID, API_HASH
from database.db import db
from typing import Optional

SESSION_STRING_SIZE = 351
LOGIN_TIMEOUT = 600

async def cleanup_session(client: Optional[Client]):
    if client:
        try:
            await client.disconnect()
            await client.stop()
        except:
            pass

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["logout"]))
async def logout(client, message):
    await db.set_session(message.from_user.id, session=None)
    await message.reply("Logged out successfully")

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["login"]))
async def login_handler(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if await db.get_session(user_id):
        return await message.reply("You're already logged in. Use /logout first")
        
    client = None
    try:
        phone_number_msg = await bot.ask(
            chat_id=user_id,
            text="Send your phone number with country code (e.g., +13124562345)",
            timeout=LOGIN_TIMEOUT
        )
        
        if phone_number_msg.text == '/cancel':
            return await phone_number_msg.reply('Process cancelled')
            
        client = Client(":memory:", API_ID, API_HASH)
        await client.connect()
        
        code = await client.send_code(phone_number_msg.text)
        
        phone_code_msg = await bot.ask(
            user_id,
            "Send OTP in format: 1 2 3 4 5",
            filters=filters.text,
            timeout=LOGIN_TIMEOUT
        )
        
        if phone_code_msg.text == '/cancel':
            return await phone_code_msg.reply('Process cancelled')
            
        await client.sign_in(
            phone_number_msg.text,
            code.phone_code_hash,
            phone_code_msg.text.replace(" ", "")
        )
        
        if client.is_connected:
            string_session = await client.export_session_string()
            if len(string_session) >= SESSION_STRING_SIZE:
                await db.set_session(user_id, string_session)
                await message.reply("Login successful!")
            else:
                await message.reply("Invalid session string")
    except Exception as e:
        await message.reply(f"Login error: {str(e)}")
    finally:
        await cleanup_session(client)
