from rest_framework import viewsets
from rest_framework.views import APIView
from telegram.error import TelegramError
from .serializers import BotSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import Bot, Market
from django.db import transaction
from telegram import Bot as TelegramBot, InlineKeyboardButton, InlineKeyboardMarkup


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

logger = logging.getLogger(__name__)

class BotViewSet(viewsets.ModelViewSet):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer

class BotRegistrationView(APIView):
    def post(self, request):
        bot_token = request.data.get('bot_token')
        bot_name = request.data.get('bot_name')
        market_id = request.data.get('market_id')
        if not bot_token or not bot_name:
            return Response({"error": "bot_token and bot_name are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            market = Market.objects.get(id=market_id)
        except Market.DoesNotExist:
            return Response({"error": "Invalid market_id."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                bot = Bot.objects.create(
                    bot_token=bot_token,
                    bot_name=bot_name,
                    market=market
                )
                telegram_bot = TelegramBot(bot_token)
                keyboard = [[InlineKeyboardButton( market.name, web_app={"url": "https://example.com"}
                )]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                telegram_bot.send_message(
                    chat_id='1579489315',
                    text="Welcome to the market!",
                    reply_markup=reply_markup
                )
            return Response({
                "bot_token": bot.bot_token,
                "bot_name": bot.bot_name,
                "market_id": bot.market.id
            }, status=status.HTTP_201_CREATED)
        except TelegramError as e:
            logger.error(f"Failed to send message: {str(e)}")
            return Response({"error": f"Failed to send message: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
