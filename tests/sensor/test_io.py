from django.core.exceptions import ValidationError
import pytest

from sensor.io import validate_datetime_fieldnames_in_lines
from sensor.io import yield_readings_in_narrow_format


SOURCES = [
    {
        "lines": [
            b"Lat=0  Lon=0  Hub-Height=160  Timezone=00.0  Terrain-Height=0.0",
            b"Computed at 100 m resolution",
            b" ",
            b"YYYYMMDD HHMM   M(m/s) D(deg) SD(m/s)  DSD(deg)  Gust3s(m/s)    T(C)    PRE(hPa)       RiNumber  VertM(m/s)",
            b"20151222 0000  20.54   211.0    1.22       0.3        21.00     11.9      992.8            0.15    0.18",
            b"20151222 0010  21.02   212.2    2.55       0.6        21.35     11.8      992.7            0.29   -0.09",
        ],
        "encoding": "utf-8",
        "delimiter": "\s+",
        "datetime_fieldnames": ["YYYYMMDD", "HHMM"],
        "datetime_formats": [r"%Y%m%d %H%M"],
        "na_values": ["NAN"],
    }
]


@pytest.mark.parametrize(
    "lines,encoding,delimiter,datetime_fieldnames",
    [
        (
            [
                b"Lat=0  Lon=0  Hub-Height=160  Timezone=00.0  Terrain-Height=0.0",
                b"Computed at 100 m resolution",
                b" "
            ],
            "utf-8",
            "\s+",
            ["YYYYMMDD", "HHMM"],
        )
    ]
)
def test_validate_datetime_fieldnames_in_lines_on_invalid_lines(
    lines,
    encoding,
    delimiter,
    datetime_fieldnames,
) -> None:
    with pytest.raises(ValidationError):
        validate_datetime_fieldnames_in_lines(
            lines=lines,
            encoding=encoding,
            delimiter=delimiter,
            datetime_fieldnames=datetime_fieldnames,
        )


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
def test_yield_readings_in_narrow_format(
    lines,
    encoding,
    delimiter,
    datetime_fieldnames,
    datetime_formats,
    snapshot,
) -> None:
    output = [
        reading 
        for reading in yield_readings_in_narrow_format(
            lines=lines,
            encoding=encoding,
            delimiter=delimiter,
            datetime_fieldnames=datetime_fieldnames,
            datetime_formats=datetime_formats,
        )
    ]
    assert output == snapshot
