# import asyncio
# from django.core.management.base import BaseCommand
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
# from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
# from telegram_bot.models import Bot  # your model
# from asgiref.sync import sync_to_async
#
#
# @sync_to_async
# def get_all_bots():
#     return list(Bot.objects.select_related("market").filter(status=True))
#
#
# async def start_bot_instance(bot_instance):
#     token = bot_instance.bot_token
#     market = bot_instance.market
#
#     async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#         keyboard = []
#         if market.web_app_url:
#             keyboard.append([
#                 InlineKeyboardButton(market.name, web_app=WebAppInfo(url=market.web_app_url))
#             ])
#         if keyboard:
#             await update.message.reply_text("Добро пожаловать! Выберите маркет:", reply_markup=InlineKeyboardMarkup(keyboard))
#         else:
#             await update.message.reply_text("Добро пожаловать! Нет доступных маркетов.")
#
#     app = ApplicationBuilder().token(token).build()
#     app.add_handler(CommandHandler("start", start))
#
#     print(f"[DEBUG] Starting bot: {bot_instance.bot_name} for market {market.name}")
#     await app.initialize()
#     await app.start()
#     await app.updater.start_polling()
#     return app
#
#
# class Command(BaseCommand):
#     help = 'Run all active Telegram Bots from DB'
#
#     def handle(self, *args, **kwargs):
#         asyncio.run(self.run_all_bots())
#
#     async def run_all_bots(self):
#         bots = await get_all_bots()
#         if not bots:
#             print("[WARNING] No active bots found to run.")
#             return
#
#         bot_tasks = [start_bot_instance(bot) for bot in bots]
#         running_bots = await asyncio.gather(*bot_tasks)
#
#         print(f"[INFO] Running {len(running_bots)} bots...")
#         try:
#             while True:
#                 await asyncio.sleep(3600)
#         except KeyboardInterrupt:
#             print("[INFO] Stopping all bots...")
#             for bot in running_bots:
#                 await bot.updater.stop()
#                 await bot.stop()

import asyncio

from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler

from telegram_bot.models import Bot


class Command(BaseCommand):
    help = 'Run all active Telegram bots with delay between each'

    def handle(self, *args, **options):
        asyncio.run(self.run_all_bots())

    @sync_to_async
    def get_active_bots(self):
        return list(Bot.objects.filter(is_active=True))

    @sync_to_async
    def get_market(self, bot):
        return bot.market

    async def run_all_bots(self):
        bots = await self.get_active_bots()

        if not bots:
            print("❌ No active bots found.")
            return

        for bot in bots:
            print(f"✅ Starting bot: {bot.bot_name}")
            asyncio.create_task(self.start_bot(bot))
            await asyncio.sleep(5)

        while True:
            await asyncio.sleep(3600)

    async def start_bot(self, bot):
        market = await self.get_market(bot)
        print(f"Запускаем бот {bot.bot_name} для маркета: {market.name}")

        app = ApplicationBuilder().token(bot.bot_token).build()

        async def start(update, context):
            message = f"👋 Hello! This is the bot for market: {market.name}"

            if market.web_app_url:
                button = InlineKeyboardButton(
                    "Open Market Web App",
                    web_app=WebAppInfo(url=market.web_app_url)
                )
                reply_markup = InlineKeyboardMarkup([[button]])
            else:
                reply_markup = None

            await update.message.reply_text(message, reply_markup=reply_markup)

        app.add_handler(CommandHandler("start", start))

        await app.initialize()
        await app.start()
        await app.updater.start_polling()
