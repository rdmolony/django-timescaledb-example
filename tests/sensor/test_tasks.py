from unittest.mock import patch

from django.core.files.base import ContentFile
import pytest

from sensor.models import File
from sensor.models import FileType
from sensor.tasks import parse_and_import_to_db


@pytest.mark.django_db
def test_parse_and_import_to_db_is_called():

    with patch("sensor.models.File.parse_and_import_to_db") as importer:
        file_obj = File.objects.create(
            file=ContentFile(b"", name="sensor-readings.txt"),
            type=FileType.objects.create(name="type")
        )
        parse_and_import_to_db(file_id=file_obj.id)

    assert importer.called, "parse_and_import_to_db was not called!"
