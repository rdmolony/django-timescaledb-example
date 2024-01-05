from rest_framework import serializers

from ..models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

    def validate(self, attrs):
        instance = File(**attrs)
        instance.clean()
        return attrs
