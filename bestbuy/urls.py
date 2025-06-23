"""
URL configuration for bestbuy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from bestbuy_app.views import DeliveryDepartmentViewSet, AdditionalMarketViewSet, GetMeView, LoginView, MarketViewSet, OrdersViewSet, RegisterView, LoginView, index_page, DashboardView, CategoryViewSet, ProductViewSet, UserViewSet, BotConfigurationViewSet, ReviewViewSet, OrderItemViewSet, RoleChoicesView, UserActivityLogsViewSet, SMSCampaignViewSet, BranchesViewSet, PaymentMethodsViewSet, VariationsViewSet
router = DefaultRouter()



# Импорт ViewSet
from bestbuy_app.views import (
    CategoryViewSet, ProductViewSet, UserViewSet, BotConfigurationViewSet,
    ReviewViewSet, OrderItemViewSet, UserActivityLogsViewSet,
    SMSCampaignViewSet, BranchesViewSet, PaymentMethodsViewSet,
    VariationsViewSet, OrdersViewSet, MarketViewSet,
    AdditionalMarketViewSet, DeliveryDepartmentViewSet,
    RegisterView, LoginView, GetMeView, RoleChoicesView, DashboardView,
    TelegramAuthView
)









schema_view = get_schema_view(
    openapi.Info(
        title="BestBuy Backend API",
        default_version='v1',
        description="Документация API для интернет-магазина BestBuy",
        contact=openapi.Contact(email="example@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'users', UserViewSet, basename='users')
router.register(r'bot-configs', BotConfigurationViewSet, basename='bot-configs')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'order-items', OrderItemViewSet, basename='order-items')
router.register(r'user-logs', UserActivityLogsViewSet, basename='user-logs')
router.register(r'sms-campaigns', SMSCampaignViewSet, basename='sms-campaigns')
router.register(r'branches', BranchesViewSet, basename='branches')
router.register(r'payment-methods', PaymentMethodsViewSet, basename='payment-methods')
router.register(r'variations', VariationsViewSet, basename='variations')
router.register(r'orders', OrdersViewSet, basename='orders')
router.register(r'markets', MarketViewSet, basename='markets')
router.register(r'additional_markets', AdditionalMarketViewSet, basename='additional_markets'),
router.register(r'delivery-departments', DeliveryDepartmentViewSet, basename='delivery-departments')
#router.register(r'telegram_auth', TelegramAuthView)

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )


from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    # Аутентификация
    path('api/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/auth/login/', LoginView.as_view(), name='auth_login'),
    path('api/auth/telegram-auth/', TelegramAuthView.as_view(), name='telegram-auth'),

    #Функция GetMe
    path('api/users/me/', GetMeView.as_view(), name='get-me'),


    # Страница ролей
    path('api/roles/', RoleChoicesView.as_view(), name='roles'),

    # Прочие API endpoint'ы
    path('api/roles/', RoleChoicesView.as_view(), name='roles'),
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),
    #path('api/', include(router.urls)),

    # Swagger и Redoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Django admin
    path('admin/', admin.site.urls),
    #path('api/', include('router.urls')),
    path('bot/', include('telegram_bot.urls')),

    # Главная страница
    path('', index_page),
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)