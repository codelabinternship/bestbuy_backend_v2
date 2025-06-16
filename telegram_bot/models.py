from django.db import models

# Create your models here.
# models.py

class Quiz(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class TelegramBotConfig(models.Model):
    contacts = models.JSONField()
    about_company = models.TextField()
    about_delivery = models.TextField()
    announcement = models.TextField()
    web_app_url = models.URLField()
    welcome_message = models.TextField()
    welcome_video = models.FileField(upload_to='welcome_videos/', null=True, blank=True)
    require_address = models.BooleanField(default=False)
    require_registration = models.BooleanField(default=False)
    market = models.ForeignKey('BestBuy_bot.Market', on_delete=models.CASCADE)

    def __str__(self):
        return f"BotConfig for market {self.market.name}"