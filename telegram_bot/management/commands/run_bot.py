from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from django.core.management.base import BaseCommand

BOT_TOKEN = ''

WEB_APP_URL = 'https://zein-demo.netlify.app/'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Открыть Best Buy", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Добро пожаловать! Нажмите кнопку ниже:', reply_markup=reply_markup)

class Command(BaseCommand):
    help = 'Run Telegram Bot'

    def handle(self, *args, **kwargs):
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler('start', start))
        app.run_polling()

