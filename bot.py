import os
import yt_dlp

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.environ["8883668525:AAFCcmKP_CF-BiFWwEumfCd8vwBWxmokMt0"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 🤖\n"
        "Отправь мне ссылку на видео."
    )


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("⏳ Скачиваю видео...")

    options = {
        "outtmpl": "video.%(ext)s",
        "format": "best[ext=mp4]/best",
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_file = ydl.prepare_filename(info)

        with open(downloaded_file, "rb") as video:
            await update.message.reply_video(video=video)

        os.remove(downloaded_file)

    except Exception as e:
        await update.message.reply_text(
            "❌ Ошибка при скачивании:\n" + str(e)
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        download_video
    )
)

print("Бот запущен 🤖")

app.run_polling()
