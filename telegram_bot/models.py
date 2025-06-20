from django.db import models
from bestbuy_app.models import Market


class Bot(models.Model):
    bot_token = models.CharField(max_length=255, unique=True)
    bot_name = models.CharField(max_length=255)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    settings = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Telegram Bot"
        verbose_name_plural = "Telegram Bots"

    def __str__(self):
            return f"{self.bot_name} ({self.market.name})"

    def start_bot(self):
        from telegram import Bot as TgBot, InlineKeyboardButton, InlineKeyboardMarkup
        from telegram.error import TelegramError

        try:
            tg_bot = TgBot(token=self.bot_token)
            keyboard = [
                [InlineKeyboardButton(text=self.market.name, web_app={"url": self.market.web_app_url})]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            tg_bot.send_message(
                chat_id="@your_channel_or_group",
                text=f"*{self.bot_name} is ready!*",
                reply_markup=markup,
                parse_mode="Markdown"
            )
            self.status = True
            self.save()
            return True
        except TelegramError as e:
            print(f"Failed to start bot {self.bot_name}: {e}")
            return False