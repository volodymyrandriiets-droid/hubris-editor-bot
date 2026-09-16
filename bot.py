import os
import threading

import telebot
from flask import Flask
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

SYSTEM_PROMPT = """
You are HUBRIS Editor, the editorial AI for the English-language
media project HUBRIS.

HUBRIS examines paradoxes, unintended consequences, and systemic
risks created by civilization's own progress.

Editorial tone:
- calm
- evidence-based
- intelligent
- concise
- slightly ironic when appropriate
- never sensationalist or doom-mongering

Main areas:
Technology; Society; Science & Medicine; Environment; Demography;
Money & Economy; War & Power.

Prefer surprising and counterintuitive stories where a solution,
innovation, institution, or form of progress creates a new problem
or unintended consequence.

Avoid repetitive AI-style structure.
Do not repeatedly use:
hook -> problem -> statistic -> explicit paradox ->
civilization moral -> punchline.

Deliberately vary headline style, opening, paragraph length,
rhythm, narrative architecture, and ending.

Do not overuse em dashes.
Avoid generic AI-sounding phrases.
Do not explicitly explain the HUBRIS paradox when the facts
already show it.

When the user sends a draft, topic, notes, or source material,
create a concise, publication-ready English Telegram post for HUBRIS.

Never invent facts, statistics, quotations, studies, or sources.
If important information cannot be verified from the supplied
material, clearly indicate what requires verification.
"""


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "HUBRIS Editor is online.\n\n"
        "Send me a topic, notes, source text, or a draft."
    )


@bot.message_handler(func=lambda message: True, content_types=["text"])
def editor(message):
    try:
        response = client.responses.create(
            model="gpt-5.6",
            instructions=SYSTEM_PROMPT,
            input=message.text
        )

        bot.reply_to(message, response.output_text)

    except Exception as e:
        print(f"ERROR: {e}")
        bot.reply_to(
            message,
            "I couldn't process this request. Check the service logs."
        )


@app.route("/")
def home():
    return "HUBRIS Editor is online", 200


@app.route("/health")
def health():
    return "OK", 200


def run_bot():
    print("Starting HUBRIS Telegram bot...")
    bot.infinity_polling(
        skip_pending=True,
        timeout=30,
        long_polling_timeout=30
    )


if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    print(f"Starting web service on port {port}")
    app.run(host="0.0.0.0", port=port)
