from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BotViewSet, BotRegistrationView

router = DefaultRouter()
router.register(r'bots', BotViewSet)

urlpatterns = [
    path('', include(router.urls)),
]