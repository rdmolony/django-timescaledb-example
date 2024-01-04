from collections import OrderedDict
import csv
from datetime import datetime
from datetime import timezone
import re
import typing

from django.core.exceptions import ValidationError


def yield_readings(
    lines: typing.Iterable[str],
    encoding: str,
    delimiter: str,
    datetime_fieldnames: typing.Iterable[str],
    datetime_formats: typing.Iterable[str],
) -> typing.Tuple[typing.Any]:

    # NOTE: replace null bytes or `\x00` with empty bytes or `b""`
    decode = lambda s: s.replace(b"\x00", b"").decode(encoding)
    split = lambda s: re.split(delimiter, s)
    standardised_lines = (
        split(decode(_line))
        for _line in enumerate(lines)
    )

    fieldnames = None

    for line in standardised_lines:

        if datetime_fieldnames in line:
            fieldnames = line
        
        if fieldnames:

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
                        yield f"{timestamp},{sensor},{reading}"


def unescape_backslash(s: str) -> str:
    """Unescape a backslash-escaped string like `\\t` to `\t`.

    Source: https://stackoverflow.com/questions/1885181/how-to-un-escape-a-backslash-escaped-string
    """
    return s.encode("utf-8", "backslashreplace").decode("unicode-escape")


def import_to_db(
    file_obj,
) -> None:

    target_table = "sensor_reading_generic"

    if not file_obj.configuration:
        message = (
            "Please define this file's configuration"
            + " before attempting to parse it"
            + " so the file's `encoding`, `delimiter`, `datetime_fieldnames`"
            + " etc are defined!"
        )
        raise ValidationError(message)

    try:
        # NOTE: ensure that the file datetime_format, encoding etc are valid!
        file_obj.clean()

        file = file_obj.file
        configuration = file_obj.configuration
        encoding = configuration.encoding
        delimiter = unescape_backslash(configuration.delimiter)
        datetime_fieldnames = configuration.datetime_fieldnames
        datetime_formats = configuration.datetime_formats
        na_values = configuration.na_values

        # NOTE: `FileViewSet::post` validates that `datetime_fieldnames` are in `file`
        fieldnames, header_row = find_fieldnames_in_file(
            file=file,
            encoding=encoding,
            datetime_fieldnames=datetime_fieldnames,
            delimiter=delimiter,
        )

        if len(fieldnames) == 0:
            raise ValidationError(f"No fieldnames found in file | File: {file_obj}")

        # NOTE: datetime fieldnames are not valid sensor names
        valid_sensor_names = set(
            [f for f in fieldnames if f not in datetime_fieldnames]
        )

        sensors = file_obj.upload_sensor_names(
            station=station, sensor_names=valid_sensor_names
        )

        columns, rows = iter_sensor_readings(
            file=file,
            station_id=station.id,
            file_id=file_obj.id,
            sensors=sensors,
            encoding=encoding,
            delimiter=delimiter,
            datetime_fieldnames=datetime_fieldnames,
            datetime_formats=datetime_formats,
            fieldnames=fieldnames,
            na_values=na_values,
            skiplines=header_row,
        )

        sql.insert(
            rows=rows,
            columns=columns,
            table=target_table,
            primary_key_columns=["station_id", "sensor_id", "timestamp"],
        )

    except Exception as e:
        file_obj.parsed = None
        file_obj.parse_error = str(e)
        file_obj.save()
        raise e

    else:
        file_obj.parsed = datetime.now(timezone.utc)
        file_obj.parse_error = None
        file_obj.save()
    
    finally:
        file_obj.save()