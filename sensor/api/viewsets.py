from rest_framework import viewsets

from ..models import File
from .serializers import FileSerializer


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.parse_and_import_to_db()
