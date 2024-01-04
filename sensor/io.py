from ast import literal_eval
from collections import OrderedDict
from datetime import datetime
from datetime import timezone
from itertools import islice
import re
import typing

from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Reading


def unescape_backslash(s: str) -> str:
    """
    Unescape a backslash-escaped string like `\\t` to `\t`.

    Source: https://stackoverflow.com/questions/1885181/how-to-un-escape-a-backslash-escaped-string
    """
    return literal_eval(f'"{s}"')


def yield_readings(
    lines: typing.Iterator[bytes],
    encoding: str,
    delimiter: str,
    datetime_fieldnames: typing.Iterable[str],
    datetime_formats: typing.Iterable[str],
) -> typing.Iterator[typing.Tuple[typing.Any]]:
    """
    Yield wide-format lines as narrow-format readings

    https://en.wikipedia.org/wiki/Wide_and_narrow_data
    """
    split = lambda s: re.split(unescape_backslash(delimiter), s)
    standardised_lines = (split(line.decode(encoding)) for line in lines)

    fieldnames = None

    for line in standardised_lines:

        if set(datetime_fieldnames).issubset(set(line)):
            fieldnames = line
            break
    
    if fieldnames == None:
        raise ValidationError(f"No `datetime_fieldnames` {datetime_fieldnames} found!")

    for line in standardised_lines:
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


def import_to_db(
    file_obj,
) -> None:

    if not file_obj.type:
        message = (
            "Please define this file's type"
            + " before attempting to parse it"
            + " so the file's `encoding`, `delimiter`, `datetime_fieldnames`"
            + " etc are defined!"
        )
        raise ValidationError(message)

    try:

        # NOTE: ensure that the file datetime_format, encoding etc are valid!
        file_obj.clean()

        with file_obj.file.open(mode="rb") as f:
            readings = yield_readings(
                lines=f,
                encoding=file_obj.type.encoding,
                delimiter=file_obj.type.delimiter,
                datetime_fieldnames=file_obj.type.datetime_fieldnames,
                datetime_formats=file_obj.type.datetime_formats,
            )

        reading_objs = (
            Reading(
                timestamp=r["timestamp"],
                sensor_name=r["sensor_name"],
                reading=r["reading"]
            )
            for r in readings
        )
        batch_size = 1_000

        with transaction.atomic():
            while True:
                batch = list(islice(reading_objs, batch_size))
                if not batch:
                    break
                Reading.objects.bulk_create(batch, batch_size)

    except Exception as e:
        file_obj.parsed = None
        file_obj.parse_error = str(e)
        file_obj.save()
        raise e

    else:
        file_obj.parsed = datetime.now(timezone.utc)
        file_obj.parse_error = None
        file_obj.save()
