from django.shortcuts import render
from rest_framework import permissions
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.inspectors import SwaggerAutoSchema
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser



class TaggedSchema(SwaggerAutoSchema):
    TAG = "Default"

    def get_tags(self, operation_keys=None):
        return [self.TAG]

class ProductSchema(TaggedSchema):
    TAG = "Products_api"

class UserSchema(TaggedSchema):
    TAG = "Users_api"

class Market_api(TaggedSchema):
    TAG = "Markets_api"

class OrderSchema(TaggedSchema):
    TAG = "Orders_api"


class DashboardSchema(TaggedSchema):
    TAG = "Dashboard_api"


class Additional_markets(TaggedSchema):
    TAG = "Additional_markets_api"

class RegisterAuth(TaggedSchema):
    TAG = "RegisterAuth_api"

class Delivery_Department(TaggedSchema):
    TAG = "Delivery_Department_api"
class Category_api(TaggedSchema):
    TAG = "Category_api"


class Bot_api(TaggedSchema):
    TAG = "Bot"
class Bot_configs_api(TaggedSchema):
    TAG = "Bot_configs"
class branches(TaggedSchema):
    TAG = "Branches"

class order_items(TaggedSchema):
    TAG = "order_items"

class Reviews_api(TaggedSchema):
    TAG = "Reviews"

class payment_metods(TaggedSchema):
    TAG = "Payment_metods"

class sms_campaigns(TaggedSchema):
    TAG = "SMS_campaigns"
class user_logs(TaggedSchema):
    TAG = "User_logs"

class variations_api(TaggedSchema):
    TAG = "Variations"






@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    # permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    swagger_schema = RegisterAuth


@method_decorator(csrf_exempt, name='dispatch')
class DashboardView(APIView):

    @swagger_auto_schema(operation_description="Get user dashboard data", manual_parameters=[
        openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
    ])
    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response({
            'message': 'Welcome to dashboard!',
            'user': user_serializer.data
        }, 200)


def index_page(request):
    return render(request, 'index.html')


# Create your views here.


from rest_framework import viewsets
from .models import AdditionalMarket, Product, Category, User, BotConfiguration, Reviews, OrderItem, RoleChoices, \
    UserActivityLogs, SMSCampaign
from .serializers import DeliveryDepartmentSerializer, RegisterSerializer, AdditionalMarketSerializer, VariationsSerializer, PaymentMethodsSerializer, \
    OrdersSerializer, ExportHistorySerializer, ChannelPostsSerializer, LoyaltyProgramSerializer, BranchesSerializer, \
    ProductSerializer, CategorySerializer, UsersSerializer, BotConfigurationSerializer, ReviewSerializer, \
    OrderItemSerializer, RoleChoicesSerializer, UserActivityLogsSerializer, SMSCampaignSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})




from rest_framework.parsers import JSONParser

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    swagger_schema = ProductSchema

    def perform_create(self, serializer):
        variations_data = self.request.data.get('variations')
        if isinstance(variations_data, str):
            try:
                variations_data = json.loads(variations_data)
            except json.JSONDecodeError:
                raise serializers.ValidationError({'variations': 'Invalid JSON format'})

        product = serializer.save()
        for var in variations_data:
            Variations.objects.create(product=product, **var)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)







@method_decorator(csrf_exempt, name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    swagger_schema = UserSchema


@method_decorator(csrf_exempt, name='dispatch')
class BotConfigurationViewSet(viewsets.ModelViewSet):
    queryset = BotConfiguration.objects.all()
    serializer_class = BotConfigurationSerializer
    swagger_schema = Bot_api


@method_decorator(csrf_exempt, name='dispatch')
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    swagger_schema = Reviews_api


@method_decorator(csrf_exempt, name='dispatch')
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    swagger_schema = order_items


@method_decorator(csrf_exempt, name='dispatch')
class RoleChoicesView(APIView):
    @swagger_auto_schema(rquery_serializer=RoleChoicesSerializer, tags=["RolechoiChoise"])
    def get(self, request):
        roles = [{"key": role.name, "value": role.value} for role in RoleChoices]
        return Response(roles, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class UserActivityLogsViewSet(viewsets.ModelViewSet):
    queryset = UserActivityLogs.objects.all().order_by('-created_at')
    serializer_class = UserActivityLogsSerializer
    swagger_schema = user_logs


class SMSCampaignViewSet(viewsets.ModelViewSet):
    queryset = SMSCampaign.objects.all()
    serializer_class = SMSCampaignSerializer
    swagger_schema = sms_campaigns


class BranchesViewSet(viewsets.ModelViewSet):
    queryset = Branches.objects.all()
    serializer_class = BranchesSerializer
    swagger_schema = branches


class PaymentMethodsViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethods.objects.all()
    serializer_class = PaymentMethodsSerializer
    swagger_schema = payment_metods


class VariationsViewSet(viewsets.ModelViewSet):
    queryset = Variations.objects.all()
    serializer_class = VariationsSerializer
    parser_class = [MultiPartParser, FormParser]
    swagger_schema = variations_api


#class UserViewSet(viewsets.ModelViewSet):
    #queryset = User.objects.all()
    #serializer_class = UserSerializer


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    swagger_schema = OrderSchema

class PaymentStatusViewSet(viewsets.ModelViewSet):
    queryset = PaymentStatus.objects.all()
    serializer_class = PaymentStatusSerializer

class OrderStatusViewSet(viewsets.ModelViewSet):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatus


class ExportHistoryViewSet(viewsets.ModelViewSet):
    queryset = ExportHistory.objects.all()
    serializer_class = ExportHistorySerializer


class ChannelPostsViewSet(viewsets.ModelViewSet):
    queryset = ChannelPosts.objects.all()
    serializer_class = ChannelPostsSerializer


class LoyaltyProgramViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyProgram.objects.all()
    serializer_class = LoyaltyProgramSerializer


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [AllowAny]
    swagger_schema = RegisterAuth

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Пользователь и магазин успешно созданы'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class MarketViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer
    permission_classes = [AllowAny]
    swagger_schema = Market_api

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    #def perform_create(self, serializer):
        #serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if request.user.is_staff:
            queryset = queryset.filter(is_active=True)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    #def perform_create(self, serializer):
        #serializer.save(owner=self.request.user)


@method_decorator(csrf_exempt, name='dispatch')
class AdditionalMarketViewSet(viewsets.ModelViewSet):
    queryset = AdditionalMarket.objects.all()
    serializer_class = AdditionalMarketSerializer
    swagger_schema = Additional_markets

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'user']
    search_fields = ['name']
    ordering_fields = ['name']


@method_decorator(csrf_exempt, name='dispatch')
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    swagger_schema = Category_api


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]
    swagger_schema = RegisterAuth

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.filter(email=email).first()
                if user and user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    user_data = UserSerializer(user).data
                    return Response(
                        {
                            "access": str(refresh.access_token),
                            "user": user_data,  # This includes 'role'
                        }
                    )
                else:
                    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить информацию о текущем пользователе",
        responses={200: UserSerializer()}, tags=["GetMe_api"]
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# ViewSet Для отдела доставки
class DeliveryDepartmentViewSet(viewsets.ModelViewSet):
    queryset = DeliveryDepartment.objects.all()
    serializer_class = DeliveryDepartmentSerializer
    permission_classes = [IsAuthenticated]
    swagger_schema = Delivery_Department

    @swagger_auto_schema(operation_description="Получить список отделов доставки")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Создать отдел доставки")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Получить отдел доставки по ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Обновить отдел доставки")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Удалить отдел доставки")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



class TelegramAuthView(APIView):
    swagger_schema = RegisterAuth
    @swagger_auto_schema(
        operation_description="Authenticate via Telegram ID",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['telegram_id'],
            properties={
                'telegram_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'user_name': openapi.Schema(type=openapi.TYPE_STRING),


            },
        ),
        responses={200: openapi.Response('User Authenticated', UserSerializer)},
    )
    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        user_name = request.data.get("user_name", f"user_{telegram_id}")
        #first_name = request.data.get("first_name", "")
        is_new = False

        if not telegram_id:
            return Response({"error": "telegram_id is required"}, status=400)

        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "user_name": user_name or f"user_{telegram_id}",
                "email": f"tg_{telegram_id}@telegram.local",
                "role": RoleChoices.CUSTOMER,
            }
        )

        is_new = created
        return Response({
            "user": UserSerializer(user).data,
            "is_new": is_new
        }, status=200)