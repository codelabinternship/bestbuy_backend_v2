from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BotViewSet

router = DefaultRouter()
router.register(r'', BotViewSet)

urlpatterns = [
    path('', include(router.urls)),
]