import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token and owner ID
BOT_TOKEN = os.getenv("BOT_TOKEN", "8466271055:AAEuITQNe4DXvSX2GFybR0oB-2cPmnc6Hs8")
OWNER_ID = 7124683213

# Flask app for Render
app = Flask(__name__)

# Telegram Application (new API v20+)
application = Application.builder().token(BOT_TOKEN).build()

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        await update.message.reply_text("✅ Hello Owner! Bot is active 24/7 on Render 🚀")
    else:
        await update.message.reply_text("❌ You are not my owner!")

application.add_handler(CommandHandler("start", start))

# Flask route for health check
@app.route("/")
def index():
    return "Bot is running on Render!", 200

# Flask route for Telegram webhook
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok", 200

# Run on Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{BOT_TOKEN}"

    # Start webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=BOT_TOKEN,
        webhook_url=webhook_url
    )
