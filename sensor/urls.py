from django.shortcuts import redirect
from django.urls import include
from django.urls import path

from . import views


app_name = "sensor"


urlpatterns = [
    path('', lambda request: redirect('sensor:upload-file')),

    path('upload-file/', views.upload_file, name="upload-file"),
]
