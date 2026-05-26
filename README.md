# football-bot
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

headers = {"x-apisports-key": API_KEY}

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ Bot działa!\n\nKomendy:\n/live - live mecze\n/value - BTTS + Over 2.5"
    )

# LIVE MATCHES
async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    r = requests.get(url, headers=headers)
    data = r.json()

    matches = data.get("response", [])

    if not matches:
        await update.message.reply_text("Brak meczów live 😔")
        return

    msg = "🔥 LIVE:\n\n"

    for m in matches[:5]:
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]
        score = m["goals"]

        msg += f"{home} {score['home']} - {score['away']} {away}\n"

    await update.message.reply_text(msg)

# VALUE MATCHES (simple BTTS / Over 2.5 logic)
async def value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    r = requests.get(url, headers=headers)
    data = r.json()

    matches = data.get("response", [])

    if not matches:
        await update.message.reply_text("Brak danych 😔")
        return

    msg = "📊 VALUE GAMES (BTTS / Over 2.5 sugerowane):\n\n"

    for m in matches[:5]:
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]
        hg = m["goals"]["home"] or 0
        ag = m["goals"]["away"] or 0
        total = hg + ag

        suggestion = ""

        if total >= 2:
            suggestion += "🔥 Over 2.5 możliwe\n"
        if hg > 0 and ag > 0:
            suggestion += "⚽ BTTS TAK\n"

        if suggestion:
            msg += f"{home} vs {away}\n{suggestion}\n"

    await update.message.reply_text(msg)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("live", live))
app.add_handler(CommandHandler("value", value))

app.run_polling()
