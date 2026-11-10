import os
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]
WEATHER_KEY = os.environ["WEATHER_KEY"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Напиши назву міста, і я покажу погоду. Наприклад: Київ")


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.strip()
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": WEATHER_KEY, "units": "metric", "lang": "ua"}

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, params=params)

    if r.status_code != 200:
        await update.message.reply_text("Не знайшов таке місто 🤔 Спробуй ще раз.")
        return

    d = r.json()
    text = (
        f"📍 {d['name']}, {d['sys']['country']}\n"
        f"🌡 {d['main']['temp']:.0f}°C (відчувається як {d['main']['feels_like']:.0f}°C)\n"
        f"☁️ {d['weather'][0]['description'].capitalize()}\n"
        f"💧 Вологість: {d['main']['humidity']}%\n"
        f"💨 Вітер: {d['wind']['speed']} м/с"
    )
    await update.message.reply_text(text)


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, weather))
app.run_polling()
