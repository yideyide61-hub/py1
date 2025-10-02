import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ChatMemberHandler, ContextTypes

# ============================
# CONFIG
# ============================
TOKEN = os.getenv("BOT_TOKEN", "8466271055:AAFOsoHuJnWCcL0UzcLtlmsNro-jnD9DbhA")  # put your bot token here or set env var
OWNER_ID = 712468321  # replace with your Telegram user ID

# ============================
# /start command
# ============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == OWNER_ID:
        await update.message.reply_text("✅ Hello Owner! Bot is active 24/7 🚀")
    else:
        await update.message.reply_text("❌ You are not my owner!")

# ============================
# Detect bot added to a group
# ============================
async def bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    adder = update.chat_member.from_user
    chat = update.chat_member.chat

    # Check if the event is about the bot
    if update.chat_member.new_chat_member.user.id == context.bot.id:
        if adder.id != OWNER_ID:
            # Notify owner
            try:
                await context.bot.send_message(
                    OWNER_ID,
                    f"⚠️ Someone ({adder.full_name}) added me to <b>{chat.title}</b>. Leaving...",
                    parse_mode="HTML"
                )
            except Exception:
                pass

            # Leave group
            await context.bot.leave_chat(chat.id)
        else:
            # If owner added -> stay and notify
            await context.bot.send_message(
                OWNER_ID,
                f"✅ You added me to <b>{chat.title}</b>. Staying here!",
                parse_mode="HTML"
            )

# ============================
# MAIN SETUP
# ============================
def main():
    application = Application.builder().token(TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start))

    # Chat member updates (when bot is added/removed)
    application.add_handler(ChatMemberHandler(bot_added, ChatMemberHandler.MY_CHAT_MEMBER))

    print("🤖 Bot is running with polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
