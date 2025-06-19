from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, BotRegistrationView

router = DefaultRouter()
router.register(r'quiz', QuizViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', BotRegistrationView.as_view(), name='bot-register')
]