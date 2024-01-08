from django.core.files.base import ContentFile
import pytest

from sensor.models import File
from sensor.models import FileType
from sensor.models import Reading

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
def test_import_to_db(
    lines,
    encoding,
    delimiter,
    datetime_fieldnames,
    datetime_formats,
    na_values,
    snapshot,
) -> None:

    file_type_obj = FileType.objects.create(
        delimiter=delimiter,
        datetime_fieldnames=datetime_fieldnames,
        datetime_formats=datetime_formats,
        na_values=na_values,
        encoding=encoding,
    )
    file = ContentFile(b"\n".join(l for l in lines), name="sensor-readings.txt")
    file_obj = File(file=file, type=file_type_obj)
    file_obj.save()

    file_obj.import_to_db()

    output = Reading.objects.all()
    assert output == snapshot
