from http import HTTPStatus
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import pytest

from sensor.models import FileType
from tests.globals import SOURCES


@pytest.mark.django_db
@pytest.mark.parametrize(
    "lines,encoding,delimiter,datetime_fieldnames,datetime_formats,na_values",
    [
        (
            source["lines"],
            source["encoding"],
            source["delimiter"],
            source["datetime_fieldnames"],
            source["datetime_formats"],
            source["na_values"],
        )
        for source in SOURCES
    ]
)
class TestUploadFile():

    def test_can_upload_a_valid_payload(
        self,
        client,
        lines,
        encoding,
        delimiter,
        datetime_fieldnames,
        datetime_formats,
        na_values,
    ):
        file_type = FileType.objects.create(
            name="type",
            encoding=encoding,
            delimiter=delimiter,
            datetime_fieldnames=datetime_fieldnames,
            datetime_formats=datetime_formats,
            na_values=na_values,
        )
        file = SimpleUploadedFile(
            name="sensor-readings.txt", content=b"\n".join(l for l in lines),
        )
        url = reverse("sensor:upload-file")
        
        response = client.post(url, {"file": file, "type": file_type.id})
        
        assert response.status_code == HTTPStatus.OK

    def test_cannot_upload_an_invalid_file(
        self,
        client,
        lines,
        encoding,
        delimiter,
        datetime_fieldnames,
        datetime_formats,
        na_values,
        snapshot,
    ):
        file_type = FileType.objects.create(
            name="type",
            encoding=encoding,
            delimiter=delimiter,
            datetime_fieldnames=datetime_fieldnames,
            datetime_formats=datetime_formats,
            na_values=na_values,
        )
        invalid_file = SimpleUploadedFile(
            name="sensor-readings.txt", content=b"I am invalid!",)
        url = reverse("sensor:upload-file")
        
        response = client.post(url, {"file": invalid_file, "type": file_type.id})

        assert response.status_code == HTTPStatus.OK
        assert response.content == snapshot

    def test_parse_and_import_to_db_is_called(
        self,
        client,
        lines,
        encoding,
        delimiter,
        datetime_fieldnames,
        datetime_formats,
        na_values,
    ):
        file_type = FileType.objects.create(
            name="type",
            encoding=encoding,
            delimiter=delimiter,
            datetime_fieldnames=datetime_fieldnames,
            datetime_formats=datetime_formats,
            na_values=na_values,
        )
        file = SimpleUploadedFile(
            name="sensor-readings.txt", content=b"\n".join(l for l in lines),
        )
        url = reverse("sensor:upload-file")
        
        with patch("sensor.models.File.import_to_db") as importer:
            client.post(url,{"file": file, "type": file_type.id})
            assert importer.called
