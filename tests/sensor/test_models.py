import datetime
import json

from django.core.files.base import ContentFile
import pytest

from sensor.models import File
from sensor.models import FileType
from sensor.models import Reading
from tests.globals import SOURCES


@pytest.mark.django_db
@pytest.mark.parametrize(
    "lines",
    [
        [
            {
                'reading': '20.54',
                'sensor_name': 'M(m/s)',
                'timestamp': str(datetime.datetime(2015, 12, 22, 0, 0)),
            },
            {
                'reading': '211.0',
                'sensor_name': 'D(deg)',
                'timestamp': str(datetime.datetime(2015, 12, 22, 0, 0)),
            },
        ]
    ]
)
def test_import_directly_to_db(
    lines,
    snapshot,
) -> None:

    file = ContentFile(json.dumps(lines), name="sensor-readings.txt")
    file_type_obj = FileType.objects.create(name="file-type")
    file_obj = File(file=file, type=file_type_obj)
    file_obj.save()

    file_obj.import_directly_to_db()

    output = Reading.objects.all()
    assert output == snapshot


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
def test_parse_and_import_to_db(
    lines,
    encoding,
    delimiter,
    datetime_fieldnames,
    datetime_formats,
    na_values,
    snapshot,
) -> None:

    file_type_obj = FileType.objects.create(
        name="file-type",
        delimiter=delimiter,
        datetime_fieldnames=datetime_fieldnames,
        datetime_formats=datetime_formats,
        na_values=na_values,
        encoding=encoding,
    )
    file = ContentFile(b"\n".join(l for l in lines), name="sensor-readings.txt")
    file_obj = File(file=file, type=file_type_obj)
    file_obj.save()

    file_obj.parse_and_import_to_db()

    output = Reading.objects.all()
    assert output == snapshot
