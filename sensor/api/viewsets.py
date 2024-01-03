from rest_framework import viewsets

from ..models import File
from .serializers import FileSerializer


class FileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer