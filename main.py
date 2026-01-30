import os
import asyncio
from pyrogram import Client, filters
from dotenv import load_dotenv
from vars import API_ID, API_HASH
from pw_api import PWTokenService

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "TokenRenewBot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

service = PWTokenService()

def is_jwt(token: str) -> bool:
    return isinstance(token, str) and token.count(".") == 2 and token.startswith("eyJ")

@app.on_message(filters.command("start"))
async def start(_, msg):
    if msg.chat.type != "private":
        return
    await msg.reply_text(
        "Welcome Dear😘💙\n\n"
        "Use Command /Baby for Renew your Any PW Token.✨"
    )

@app.on_message(filters.command("Baby"))
async def baby(_, msg):
    if msg.chat.type != "private":
        return
    await msg.reply_text("SEND ME YOUR CURRENT TOKEN")

@app.on_message(filters.text & ~filters.command)
async def process_token(_, msg):
    if msg.chat.type != "private":
        return

    old_token = msg.text.strip()
    if not is_jwt(old_token):
        await msg.reply_text("❌ INVALID TOKEN FORMAT")
        return

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

    try:
        new_token = await service.renew_token(old_token)

        await asyncio.sleep(1)
        await start_message.edit_text(
            "Progress: [🟩🟩🟩🟩🟩🟩🟩🟩🟩] 100%"
        )

        await msg.reply_text(
            f"NEW TOKEN (very useful):\n\n{new_token}"
        )

        await msg.reply_text(
            "THANK YOU FOR USING ME\n\n"
            "BOT MAD BY: @SmartBoy_ApnaMS"
        )

    except Exception:
        await msg.reply_text("❌ TOKEN RENEW FAILED")

app.run()
