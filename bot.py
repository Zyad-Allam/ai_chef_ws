import os
import asyncio
import httpx
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()  # Load environment variables from .env file
API_URL = "http://127.0.0.1:5000/ask/"
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your AI Chef bot 🍽️")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    user_id = update.message.from_user.id

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(
            API_URL, json={"action": "ask", "query": user_msg, "user_id": str(user_id)}
        )

    api_response = response.json()
    await update.message.reply_text(str(api_response))


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
