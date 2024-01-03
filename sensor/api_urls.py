from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import viewsets


app_name = "sensor"


router = DefaultRouter()
router.register('file', viewsets.FileViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
