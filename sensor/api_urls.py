from django.urls import include
from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .api import viewsets


app_name = "sensor"


file_list = viewsets.FileViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
file_detail = viewsets.FileViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'files': reverse('api:sensor:file-list', request=request, format=format),
        'echo': reverse('api:sensor:echo', request=request, format=format),
    })


urlpatterns = [
    path('', api_root, name="api-root"),
    path('file/', file_list, name='file-list'),
    path('file/<int:pk>/', file_detail, name='file-detail'),
]
