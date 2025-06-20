from rest_framework import serializers

from bestbuy_app.models import Market
from .models import Quiz, Bot


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ['bot_token', 'bot_name', 'market']

        def validate_market(self, market):
            if not Market.objects.filter(id=market.id).exists():
                raise serializers.ValidationError("Invalid market_id.")
            return market