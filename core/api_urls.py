from django.urls import include
from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


app_name = "api"


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'sensors': reverse('api:sensor:api-root', request=request, format=format),
    })


urlpatterns = [
    path('', api_root, name="api-root"),
    path('sensor/', include('sensor.api_urls'), name='sensor'),
]
