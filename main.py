import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 7124683213

# Flask app (keeps Render happy)
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "🤖 Bot is running with polling!"

# Telegram bot
application = Application.builder().token(TOKEN).build()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        await update.message.reply_text("✅ Hello Owner! Bot is active (polling mode).")
    else:
        await update.message.reply_text("❌ You are not my owner!")

application.add_handler(CommandHandler("start", start))

# Run bot with polling
async def run_bot():
    print("🚀 Bot started with polling...")
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    # Run Flask + Polling together
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())  # Run Telegram bot
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))  # Run Flask
