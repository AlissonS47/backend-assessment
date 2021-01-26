from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)
from .api.viewsets import UserRegistrationViewSet


router = routers.DefaultRouter()
router.register(r'users/registration', UserRegistrationViewSet,
                basename='user_registration')

urlpatterns = [
    path('', include(router.urls)),
    path('users/login/', TokenObtainPairView.as_view(), 
         name='token_obtain_pair'),
    path('users/login/refresh/', TokenRefreshView.as_view(), 
         name='token_refresh'),
]
