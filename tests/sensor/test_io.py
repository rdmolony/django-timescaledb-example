from django.core.files.base import ContentFile
import pytest

from sensor.io import import_to_db
from sensor.io import unescape_backslash
from sensor.io import yield_readings
from sensor.models import File
from sensor.models import FileType
from sensor.models import Reading


SOURCES = [
    {
        "lines": iter(
            [
                b"Lat=0  Lon=0  Hub-Height=160  Timezone=00.0  Terrain-Height=0.0",
                b"Computed at 100 m resolution",
                b" ",
                b"YYYYMMDD HHMM   M(m/s) D(deg) SD(m/s)  DSD(deg)  Gust3s(m/s)    T(C)    PRE(hPa)       RiNumber  VertM(m/s)",
                b"20151222 0000  20.54   211.0    1.22       0.3        21.00     11.9      992.8            0.15    0.18",
                b"20151222 0010  21.02   212.2    2.55       0.6        21.35     11.8      992.7            0.29   -0.09",
            ]
        ),
        "encoding": "utf-8",
        "delimiter": "\s+",
        "datetime_fieldnames": ["YYYYMMDD", "HHMM"],
        "datetime_formats": [r"%Y%m%d %H%M"],
        "na_values": ["NAN"],
    }
]


@pytest.mark.parametrize("string,expected", [("\\t", "\t")])
def test_unescape_backslash(string, expected):
    assert unescape_backslash(string) == expected


@pytest.mark.parametrize(
    "lines,encoding,delimiter,datetime_fieldnames,datetime_formats",
    [
        (
            source["lines"],
            source["encoding"],
            source["delimiter"],
            source["datetime_fieldnames"],
            source["datetime_formats"]
        )
        for source in SOURCES
    ]
)
def test_yield_readings(
    lines,
    encoding,
    delimiter,
    datetime_fieldnames,
    datetime_formats,
    snapshot,
) -> None:
    output = [
        reading 
        for reading in yield_readings(
            lines=lines,
            encoding=encoding,
            delimiter=delimiter,
            datetime_fieldnames=datetime_fieldnames,
            datetime_formats=datetime_formats,
        )
    ]
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
    file = ContentFile(
        b"\n".join(l for l in lines), name="sensor-readings.txt"
    )
    file_obj = File(
        file=file,
        type=file_type_obj,
    )
    import_to_db(file_obj)