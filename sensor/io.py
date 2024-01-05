from collections import OrderedDict
from datetime import datetime
import re
import typing

from django.core.exceptions import ValidationError


def yield_split_lines(
    lines: typing.Iterable[bytes],
    encoding: str,
    delimiter: str,
) -> typing.Iterator[typing.Tuple[typing.Any]]:

    # Unescape strings `\\t` to `\t` for use in a regular expression
    # https://stackoverflow.com/questions/1885181/how-to-un-escape-a-backslash-escaped-string
    unescape_backslash = lambda s: (
        s.encode('raw_unicode_escape').decode('unicode_escape')
    )
    split = lambda s: re.split(unescape_backslash(delimiter), s)
    return (split(line.decode(encoding)) for line in iter(lines))


def validate_datetime_fieldnames_in_lines(
    lines: typing.Iterable[bytes],
    encoding: str,
    delimiter: str,
    datetime_fieldnames: typing.Iterable[str],
) -> None:

    fieldnames = None

    for line in yield_split_lines(lines=lines, encoding=encoding, delimiter=delimiter):
        if set(datetime_fieldnames).issubset(set(line)):
            fieldnames = line
            break
    
    if fieldnames == None:
        raise ValidationError(f"No `datetime_fieldnames` {datetime_fieldnames} found!")


def yield_readings_in_narrow_format(
    lines: typing.Iterable[bytes],
    encoding: str,
    delimiter: str,
    datetime_fieldnames: typing.Iterable[str],
    datetime_formats: typing.Iterable[str],
) -> typing.Iterator[typing.Tuple[typing.Any]]:
    """
    https://en.wikipedia.org/wiki/Wide_and_narrow_data
    """

    split_lines = yield_split_lines(lines=lines, encoding=encoding, delimiter=delimiter)
    fieldnames = None

    for line in split_lines:
        if set(datetime_fieldnames).issubset(set(line)):
            fieldnames = line
            break
    
    if fieldnames == None:
        raise ValidationError(f"No `datetime_fieldnames` {datetime_fieldnames} found!")

    # NOTE: `split_lines` is an iterator so prior loop exhausts the header lines
    for line in split_lines:
        fields = OrderedDict([(f, v) for f, v in zip(fieldnames, line)])
        readings = OrderedDict(
            [(f, v) for f, v in fields.items() if f not in datetime_fieldnames]
        )

        timestamp_strs = [fields[k] for k in datetime_fieldnames]
        timestamp_str = " ".join(
            str(item) for item in timestamp_strs if item is not None
        )

        for datetime_format in datetime_formats:
            try:
                timestamp = datetime.strptime(timestamp_str, datetime_format)
            except ValueError:
                pass
            else:
                for sensor, reading in readings.items():
                    yield {
                        "timestamp": timestamp,
                        "sensor_name": sensor,
                        "reading": reading,
                    }
