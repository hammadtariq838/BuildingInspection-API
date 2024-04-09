from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
  path('login', TokenObtainPairView.as_view(), name='login'),
  path('refresh', TokenRefreshView.as_view(), name='refresh'),
  path('register', CreateUserView.as_view(), name='register'),
]