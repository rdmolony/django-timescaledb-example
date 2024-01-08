from rest_framework import serializers

from ..models import File
from ..models import FileType


class FileSerializer(serializers.ModelSerializer):

    type = serializers.SlugRelatedField(
        slug_field="name", queryset=FileType.objects.all()
    )

    class Meta:
        model = File
        fields = '__all__'

    def validate(self, attrs):
        instance = File(**attrs)
        instance.clean()
        return attrs
