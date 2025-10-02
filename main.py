import os
from telegram import Update, ChatMemberUpdated
from telegram.ext import Application, CommandHandler, ChatMemberHandler, ContextTypes
from flask import Flask

# ======================
# CONFIG
# ======================
TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")   # Replace with env or paste directly
OWNER_ID = 7124683213                                  # Replace with your Telegram ID
PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)

@app.route("/")
def index():
    return "🤖 Bot is running with polling!"

# ======================
# BOT SETUP
# ======================
application = Application.builder().token(TOKEN).build()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        await update.message.reply_text("✅ Hello Owner! Bot is active 24/7 on Render 🚀")
    else:
        await update.message.reply_text("❌ You are not my owner!")

# Detect when bot is added to a group
async def bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member: ChatMemberUpdated = update.chat_member
    if chat_member.new_chat_member.user.id == context.bot.id:  # Bot itself added
        adder_id = chat_member.from_user.id
        chat_id = chat_member.chat.id

        if adder_id != OWNER_ID:
            # Notify the owner in private
            await context.bot.send_message(
                OWNER_ID,
                f"⚠️ Someone (ID: {adder_id}) tried to add me to group: {chat_member.chat.title}. I left immediately."
            )
            # Leave the group
            await context.bot.leave_chat(chat_id)

# Handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(ChatMemberHandler(bot_added, ChatMemberHandler.MY_CHAT_MEMBER))

# ======================
# RUN BOT + FLASK
# ======================
import threading

def run_flask():
    app.run(host="0.0.0.0", port=PORT)

threading.Thread(target=run_flask).start()
application.run_polling()
