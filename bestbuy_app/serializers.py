from django.db import transaction
from rest_framework import serializers
from rest_framework.permissions import AllowAny

from .models import Variations, DeliveryDepartment, AdditionalMarket, User, Variations, PaymentMethods, Orders, ExportHistory, ChannelPosts, LoyaltyProgram, Branches, Market, Product, Category, BotConfiguration, Reviews, OrderItem, RoleChoices, TransactionTypeChoices, UserActivityLogs, SMSCampaign, OrderStatus, PaymentStatus
import json




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['telegram_id', 'id', 'user_name', 'email', 'created_at', 'role', 'status']


class RegisterSerializer(serializers.ModelSerializer):
    market_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['user_name', 'phone_number', 'email', 'password', 'market_name', 'id']

    def validate(self, data):

        if User.objects.filter(id=data.get('id')).exists():
            raise serializers.ValidationError({"user id": "User ID must be unique."})
        return data

    def create(self, validated_data):
        market_name = validated_data.pop('market_name')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        Market.objects.create(user=user, name=market_name)

        return user
class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'
        read_only_fields = ['owner']


class AdditionalMarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalMarket
        fields = ['id', 'user', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

#class VariationSerializer(serializers.ModelSerializer):
    #class Meta:
        #model = Variations
        #fields = ['option_name', 'option_value']




class VariationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variations
        fields = '__all__'
class ProductSerializer(serializers.ModelSerializer):
    variations = serializers.CharField(write_only=True)
    media = serializers.ImageField()
#dnnnnnxyjxmckccmcmcmmccmmfmfmfmfmfmf
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'discount_price', 'stock_quantity',
            'category', 'brand', 'media', 'created_at', 'updated_at', 'variations', 'product_id'
        ]

    def create(self, validated_data):
        from django.db import transaction


        variations_json = validated_data.pop('variations')
        try:
            variations_data = json.loads(variations_json)
        except json.JSONDecodeError:
            raise serializers.ValidationError({"variations": "Неверный JSON формат"})

        with transaction.atomic():
            product = Product.objects.create(**validated_data)
            for var_data in variations_data:
                Variations.objects.create(product=product, **var_data)

        return product

    def update(self, instance, validated_data):
        variations_json = validated_data.pop('variations', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if variations_json:
            try:
                variations_data = json.loads(variations_json)
            except json.JSONDecodeError:
                raise serializers.ValidationError({"variations": "Неверный JSON формат"})

            instance.variations.all().delete()
            for var_data in variations_data:
                Variations.objects.create(product=instance, **var_data)

        return instance

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BotConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotConfiguration
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class RoleChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleChoices
        fields = '__all__'





class UserActivityLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivityLogs
        fields = '__all__'


class SMSCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSCampaign
        fields = '__all__'



##
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class ExportHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportHistory
        fields = '__all__'

class ChannelPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelPosts
        fields = '__all__'

class LoyaltyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyProgram
        fields = '__all__'

class BranchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = '__all__'

class PaymentMethodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethods
        fields = '__all__'







#Сериализатор для отдела доставки
class DeliveryDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryDepartment
        fields = '__all__'


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'

class PaymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentStatus
        fields = '__all__'