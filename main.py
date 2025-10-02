import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 7124683213
RENDER_URL = os.getenv("RENDER_EXTERNAL_HOSTNAME")

# Flask app
flask_app = Flask(__name__)

# Telegram bot
application = Application.builder().token(TOKEN).build()

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        await update.message.reply_text("✅ Hello Owner! Bot is active 24/7 on Render.")
    else:
        await update.message.reply_text("❌ You are not my owner!")

application.add_handler(CommandHandler("start", start))

# Flask route
@flask_app.route("/")
def index():
    return "🤖 Bot is running on Render!"

# Webhook setup
@flask_app.before_first_request
def init_webhook():
    url = f"https://{RENDER_URL}/{TOKEN}"
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        url_path=TOKEN,
        webhook_url=url,
    )

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
