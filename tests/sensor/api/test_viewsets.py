from http import HTTPStatus

from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from rest_framework.reverse import reverse

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
        url = reverse("api:sensor:file-list")
        
        response = client.post(
            url,
            {"file": file, "type": file_type.name}
        )
        
        assert response.status_code == HTTPStatus.CREATED

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
        url = reverse("api:sensor:file-list")
        
        response = client.post(
            url,
            {"file": invalid_file, "type": file_type.name}
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.content == snapshot


    def test_cannot_upload_a_missing_file_type(
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
        file = SimpleUploadedFile(
            name="sensor-readings.txt", content=b"\n".join(l for l in lines),
        )
        url = reverse("api:sensor:file-list")
        
        response = client.post(
            url,
            {"file": file, "type": ""}
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.content == snapshot
