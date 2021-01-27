from django.urls import path, include
from rest_framework import routers
from .api.viewsets import RequestViewSet


router = routers.DefaultRouter()
router.register(r'requests', RequestViewSet, basename='requests')

urlpatterns = [
    path('', include(router.urls)),
]
