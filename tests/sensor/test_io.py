from datetime import datetime

import pytest

from sensor.io import unescape_backslash
from sensor.io import yield_readings


@pytest.mark.parametrize("string,expected", [("\\t", "\t")])
def test_unescape_backslash(string, expected):
    assert unescape_backslash(string) == expected


@pytest.mark.parametrize(
    "lines,delimiter,datetime_fieldnames,datetime_formats",
    [
        (
            iter(
                [
                    "Lat=0  Lon=0  Hub-Height=160  Timezone=00.0  Terrain-Height=0.0",
                    "Computed at 100 m resolution",
                    " ",
                    "YYYYMMDD HHMM   M(m/s) D(deg) SD(m/s)  DSD(deg)  Gust3s(m/s)    T(C)    PRE(hPa)       RiNumber  VertM(m/s)",
                    "20151222 0000  20.54   211.0    1.22       0.3        21.00     11.9      992.8            0.15    0.18",
                    "20151222 0010  21.02   212.2    2.55       0.6        21.35     11.8      992.7            0.29   -0.09",
                ]
            ),
            "\s+",
            ["YYYYMMDD", "HHMM"],
            [r"%Y%m%d %H%M"],
        ),
    ]
)
def test_yield_readings(
    lines,
    delimiter,
    datetime_fieldnames,
    datetime_formats,
    snapshot,
) -> None:
    output = [
        reading 
        for reading in yield_readings(
            lines=lines,
            delimiter=delimiter,
            datetime_fieldnames=datetime_fieldnames,
            datetime_formats=datetime_formats,
        )
    ]
    assert output == snapshot
