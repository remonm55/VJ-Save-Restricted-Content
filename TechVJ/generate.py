# ... [Keep original header] ...

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["login"]))
async def main(bot: Client, message: Message):
    # ... [Keep original logic until string session generation] ...
    
    try:
        async with Client(":memory:", session_string=string_session, 
                        api_id=API_ID, api_hash=API_HASH) as uclient:
            await db.set_session(message.from_user.id, session=string_session)
    except Exception as e:
        return await message.reply_text(f"Login Error: {e}")
    finally:
        if 'uclient' in locals():
            await uclient.disconnect()
    
    await bot.send_message(message.from_user.id, "Login successful!")

# ... [Keep logout command] ...
