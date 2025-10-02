import os
from telegram.ext import Application, ChatMemberHandler, CommandHandler, ContextTypes
from telegram import Update
from flask import Flask

# ==============================
# CONFIG
# ==============================
TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
OWNER_ID = 7124683213   # 👈 Replace with your Telegram user ID
PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)

@app.route("/")
def index():
    return "🤖 Bot is running with polling!"

# ==============================
# BOT SETUP
# ==============================
application = Application.builder().token(TOKEN).build()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        await update.message.reply_text("✅ Hello Owner! Bot is active 24/7 on Render 🚀")
    else:
        await update.message.reply_text("❌ You are not my owner!")

# Detect when bot is added to a group
async def bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = update.my_chat_member
    new_status = chat_member.new_chat_member.status

    # Bot just became a member of a group
    if new_status == "member":
        inviter = chat_member.from_user
        chat = chat_member.chat

        if inviter.id != OWNER_ID:
            # Notify owner privately
            msg = (
                f"⚠️ Unauthorized Add Attempt!\n\n"
                f"👤 User: {inviter.first_name} (ID: {inviter.id})\n"
                f"👥 Group: {chat.title or chat.first_name} (ID: {chat.id})\n"
                f"❌ Bot has left the group automatically."
            )
            await context.bot.send_message(OWNER_ID, msg)

            # Leave the group
            await context.bot.leave_chat(chat.id)
        else:
            await context.bot.send_message(chat.id, "✅ Added by my Owner!")

# ==============================
# HANDLERS
# ==============================
application.add_handler(CommandHandler("start", start))
application.add_handler(ChatMemberHandler(bot_added, chat_member_types=["my_chat_member"]))

# ==============================
# RUN POLLING
# ==============================
async def run_polling():
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.updater.idle()

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(run_polling())
    app.run(host="0.0.0.0", port=PORT)
