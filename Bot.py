from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import requests
import os  # ← Añade esta línea si usarás variables de entorno

TOKEN_TELEGRAM = os.getenv("TOKEN_TELEGRAM", "7830709654:AAGNyyK_Z1IIUhPCxC5XOv9ojmzsIv81xyk")  # Usa tu token
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

async def start(update: Update, context):
    await update.message.reply_text("🤖 ¡Hola! Soy tu bot con IA de DeepSeek. Pregúntame lo que quieras.")

async def handle_message(update: Update, context):
    user_message = update.message.text
    headers = {"Authorization": "Bearer free"}
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": user_message}]
    }
    try:
        response = requests.post(DEEPSEEK_API_URL, json=data, headers=headers).json()
        await update.message.reply_text(response["choices"][0]["message"]["content"])
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

app = Application.builder().token(TOKEN_TELEGRAM).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
