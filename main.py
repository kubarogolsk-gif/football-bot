import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")

if not TOKEN or not API_KEY:
    raise ValueError("TOKEN and API_KEY must be set in .env file")

headers = {
    'x-apisports-key': API_KEY
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ Football Bot działa!")

async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = "https://v3.football.api-sports.io/fixtures?live=all"

    response = requests.get(url, headers=headers)

    data = response.json()

    matches = data["response"]

    if len(matches) == 0:
        await update.message.reply_text("Brak meczów live.")
        return

    message = "⚽ MECZE LIVE:\n\n"

    for match in matches[:5]:

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        goals_home = match["goals"]["home"]
        goals_away = match["goals"]["away"]

        message += f"{home} {goals_home}-{goals_away} {away}\n"

    await update.message.reply_text(message)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("live", live))

print("Bot działa...")

app.run_polling()
