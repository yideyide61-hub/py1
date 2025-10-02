import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, ChatMemberHandler

# Bot Token & Owner ID
TOKEN = os.getenv("BOT_TOKEN", "8466271055:AAEuITQNe4DXvSX2GFybR0oB-2cPmnc6Hs8")
OWNER_ID = 7124683213

# Flask app (keep-alive for Render)
app = Flask(__name__)

@app.route("/")
def index():
    return "🤖 Bot is running with polling!"

# Telegram Bot
application = Application.builder().token(TOKEN).build()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        await update.message.reply_text("✅ Hello Owner! Bot is active 24/7 on Render 🚀")
    else:
        await update.message.reply_text("❌ You are not my owner!")

# When bot is added/removed
async def bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = update.my_chat_member

    # Check if the update is about the bot itself
    if chat_member.new_chat_member.user.id == context.bot.id:
        inviter = chat_member.from_user
        chat = chat_member.chat

        if inviter.id != OWNER_ID:
            # Notify the owner privately
            msg = (
                f"⚠️ Someone tried to add me!\n\n"
                f"👤 User: {inviter.first_name} (ID: {inviter.id})\n"
                f"👥 Group: {chat.title or chat.first_name} (ID: {chat.id})\n"
                f"❌ I left automatically."
            )
            await context.bot.send_message(OWNER_ID, msg)

            # Leave the group immediately
            await context.bot.leave_chat(chat.id)

        else:
            # If owner added → stay and greet
            await context.bot.send_message(chat.id, "✅ 由我的主人添加！")

# Handlers
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
