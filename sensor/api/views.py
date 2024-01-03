from rest_framework.decorators import api_view
from rest_framework.response import Response

from .. import tasks


@api_view(["GET"])
def echo(request, format=None):
    tasks.echo.delay()
    return Response("Echo!")
    