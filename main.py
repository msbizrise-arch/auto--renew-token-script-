import os
import asyncio
from pyrogram import Client, filters
from dotenv import load_dotenv
from vars import API_ID, API_HASH

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "TokenRenewBot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

@app.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply_text(
        "Welcome Dear😘💙\n\n"
        "Use Command /Baby for Renew your Any PW Token.✨"
    )

@app.on_message(filters.command("Baby"))
async def baby(_, msg):
    await msg.reply_text("SEND ME YOUR CURREN TOKEN")

@app.on_message(filters.text & ~filters.command)
async def process_token(_, msg):
    start_message = await msg.reply_text(
        "Progress: [⬜⬜⬜⬜⬜⬜⬜⬜⬜] 0%"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        "Progress: [🟥🟥🟥⬜⬜⬜⬜⬜⬜] 25%"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        "Progress: [🟧🟧🟧🟧🟧⬜⬜⬜⬜] 50%"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        "Progress: [🟨🟨🟨🟨🟨🟨🟨⬜⬜] 75%"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        "Progress: [🟩🟩🟩🟩🟩🟩🟩🟩🟩] 100%"
    )

    old_token = msg.text.strip()
    new_token = old_token + "_RENEWED"

    await msg.reply_text(
        f"NEW TOKEN (very useful):\n\n{new_token}"
    )

    await msg.reply_text(
        "THANK YOU FOR USING ME\n\n"
        "BOT MAD BY: @SmartBoy_ApnaMS"
    )

app.run()
