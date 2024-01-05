from django.forms import ModelForm

from .models import File
from .models import FileType


class FileForm(ModelForm):
    class Meta:
        model = File
        fields = "__all__"

class FileTypeForm(ModelForm):
    class Meta:
        model = FileType
        fields = "__all__"
