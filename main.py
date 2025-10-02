import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, ChatMemberHandler

TOKEN = os.getenv("BOT_TOKEN", "your-bot-token-here")
OWNER_ID = 7124683213  # Replace with your Telegram user ID

# Flask just to keep Render alive
app = Flask(__name__)

@app.route("/")
def index():
    return "🤖 Bot is running with polling!"

# Telegram bot setup
application = Application.builder().token(TOKEN).build()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is active and running!")

# Handle when bot is added to a chat
async def bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = update.my_chat_member
    if chat_member.new_chat_member.user.id == context.bot.id:  # The bot itself
        inviter = chat_member.from_user.id
        if inviter != OWNER_ID:
            # Not owner → leave the group
            await context.bot.leave_chat(chat_member.chat.id)
        else:
            await context.bot.send_message(chat_member.chat.id, "✅ Hello, Owner! I'm here.")

# Register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(ChatMemberHandler(bot_added, chat_member_types=["member", "administrator"]))

# Run polling in background
async def run_polling():
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.updater.idle()

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(run_polling())
    app.run(host="0.0.0.0", port=10000)
