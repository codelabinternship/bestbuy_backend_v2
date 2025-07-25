from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TelegramAuthView, MarketViewSet, DeliveryDepartmentViewSet, LoyaltyProgramViewSet, \
    ChannelPostsViewSet, ExportHistoryViewSet, OrdersViewSet, VariationsViewSet, PaymentMethodsViewSet, BranchesViewSet, \
    ProductViewSet, CategoryViewSet, UserViewSet, BotConfigurationViewSet, ReviewViewSet, OrderItemViewSet, \
    RoleChoicesView, UserActivityLogsViewSet, SMSCampaignViewSet
from django.conf import settings
from django.conf.urls.static import static
from .views import *
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'orders', OrdersViewSet)
router.register(r'export-history', ExportHistoryViewSet)
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet)
router.register(r'bot-configs', BotConfigurationViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'orderitem', OrderItemViewSet)
router.register(r'user-activity-logs', UserActivityLogsViewSet)
router.register(r'sms-campaigns', SMSCampaignViewSet)
router.register(r'branches', BranchesViewSet)
router.register(r'payment-methods', PaymentMethodsViewSet)
router.register(r'variations', VariationsViewSet)
router.register(r'channel-posts', ChannelPostsViewSet)
router.register(r'loyalty', LoyaltyProgramViewSet)
router.register(r'markets', MarketViewSet, basename='market')
router.register(r'delivery-departments', DeliveryDepartmentViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('api/auth/me/', GetMeView.as_view(), name='get_me'),
    path('auth/telegram-auth/', TelegramAuthView.as_view(), name='telegram-auth'),
    path('transactions-report/', TransactionReportView.as_view(), name='transactions-report'),
    path('report/first-user-order/', FirstOrderUserReport.as_view()),

]