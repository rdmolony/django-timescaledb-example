from django.urls import path

from . import views


app_name = "sensor"


urlpatterns = [
    path('', views.index, name="root"),

    path('create-file-type/', views.create_file_type, name="create-file-type"),
    path('upload-file/', views.upload_file, name="upload-file"),
]
