import os
import random
import string
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("Error: BOT_TOKEN is not set in environment variables.")
    exit(1)

user_login_codes = {}

def generate_login_code(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    login_code = generate_login_code()
    user_login_codes[user_id] = login_code
    await update.message.reply_text(f"Welcome! Your login code is: {login_code}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_code = user_login_codes.get(user_id)
    message_text = update.message.text.strip()

    if message_text == user_code:
        contact_button = KeyboardButton(text="Share Contact", request_contact=True)
        reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "Thank you for entering the correct login code! Please share your contact with us.",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(f"You said: {message_text}")

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if contact:
        first_name = contact.first_name or "User"
        await update.message.reply_text(
            f"Thanks for sharing your contact, {first_name}! Here is the link to our bot and channel:\n\n"
            f"Bot: https://t.me/your_bot_username\n"
            f"Channel: https://t.me/your_channel_username"
        )
    else:
        await update.message.reply_text("No contact information received.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))

    print("Bot started successfully")
    app.run_polling()

if __name__ == "__main__":
    main()
