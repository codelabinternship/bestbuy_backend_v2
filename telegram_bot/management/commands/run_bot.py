# from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
# from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
# from django.core.management.base import BaseCommand
#
# BOT_TOKEN = '7761733261:AAGFLNfXgW8oxiNxqN8BlhgsNM9kdvtOwjI'
#
# WEB_APP_URL = 'https://zein-demo.netlify.app/'
#
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [KeyboardButton("Открыть Best Buy", web_app=WebAppInfo(url=WEB_APP_URL))]
#     ]
#     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
#     await update.message.reply_text('Добро пожаловать! Нажмите кнопку ниже:', reply_markup=reply_markup)
#
# class Command(BaseCommand):
#     help = 'Run Telegram Bot'
#
#     def handle(self, *args, **kwargs):
#         app = ApplicationBuilder().token(BOT_TOKEN).build()
#         app.add_handler(CommandHandler('start', start))
#         app.run_polling()


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async

from telegram_bot.models import Market  # or your correct import
BOT_TOKEN = '7761733261:AAGFLNfXgW8oxiNxqN8BlhgsNM9kdvtOwjI'

@sync_to_async
def get_all_markets():
    return list(Market.objects.all())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markets = await get_all_markets()
    keyboard = [[
        InlineKeyboardButton(market.name, web_app=WebAppInfo(url=market.web_app_url))
        for market in markets
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Добро пожаловать! Выберите маркет:', reply_markup=reply_markup)

class Command(BaseCommand):
    help = 'Run Telegram Bot'

    def handle(self, *args, **kwargs):
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler('start', start))
        app.run_polling()
