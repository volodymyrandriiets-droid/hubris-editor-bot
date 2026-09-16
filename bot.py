import os
import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "HUBRIS Editor is online.\n\n"
        "Send me a draft and I'll prepare it for the HUBRIS workflow."
    )


@bot.message_handler(func=lambda message: True)
def receive_draft(message):
    bot.reply_to(
        message,
        f"Draft received.\n\n{message.text}"
    )


print("HUBRIS Editor Bot is running...")
bot.infinity_polling(skip_pending=True)
