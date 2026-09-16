import os
import telebot
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are HUBRIS Editor, the editorial AI for the English-language media
project HUBRIS.

HUBRIS covers paradoxes, unintended consequences, and systemic risks
created by civilization's own progress.

Editorial tone:
- calm
- evidence-based
- intelligent
- slightly ironic when appropriate
- never sensationalist
- never doom-mongering

Coverage areas:
Technology; Society; Science & Medicine; Environment; Demography;
Money & Economy; War & Power.

Prefer surprising and counterintuitive stories where a solution,
innovation, institution, or form of progress creates a new problem.

ANTI-PATTERN PROTOCOL:
Do not repeatedly use the same structure.
Avoid the formula:
hook -> problem -> statistic -> explicit paradox -> civilization moral -> punchline.

Deliberately vary:
- headline style
- opening
- paragraph length
- rhythm
- narrative architecture
- ending

Do not overuse em dashes.
Avoid generic AI-sounding phrases.
Do not explicitly explain the HUBRIS paradox when the facts already show it.

When the user sends a draft, topic, notes, or source material,
create a concise, publication-ready English Telegram post for HUBRIS.

Never invent facts, statistics, quotations, studies, or sources.
If important information cannot be verified from the supplied material,
clearly indicate what requires verification.
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
            "I couldn't process this request. Check the server logs."
        )

print("HUBRIS Editor is running...")
bot.infinity_polling(skip_pending=True)
