from django.shortcuts import redirect
from django.urls import include
from django.urls import path

from . import views


app_name = "sensor"


urlpatterns = [
    path('', lambda request: redirect('sensor:upload-file')),

    path('upload-file/', views.upload_file, name="upload-file"),
    path(
        'report-file-upload-success/',
        views.report_file_upload_success,
        name="report-file-upload-success"
    ),
    path(
        'report-file-upload-failure/',
        views.report_file_upload_failure,
        name="report-file-upload-failure"
    ),
]
