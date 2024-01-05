from django.shortcuts import redirect
from django.urls import path

from . import views


app_name = "sensor"


urlpatterns = [
    path('', views.index),

    path('create-file-type/', views.upload_file, name="create-file-type"),
    path('upload-file/', views.upload_file, name="upload-file"),
]
