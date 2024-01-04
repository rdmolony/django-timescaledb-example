from ast import literal_eval
from collections import OrderedDict
from datetime import datetime
from datetime import timezone
import re
import typing

from django.core.exceptions import ValidationError

from .models import Reading


def unescape_backslash(s: str) -> str:
    """
    Unescape a backslash-escaped string like `\\t` to `\t`.

    Source: https://stackoverflow.com/questions/1885181/how-to-un-escape-a-backslash-escaped-string
    """
    return literal_eval(f'"{s}"')


def yield_readings(
    lines: typing.Iterator[str],
    delimiter: str,
    datetime_fieldnames: typing.Iterable[str],
    datetime_formats: typing.Iterable[str],
) -> typing.Iterator[typing.Tuple[typing.Any]]:
    """
    Yield wide-format lines as narrow-format readings

    https://en.wikipedia.org/wiki/Wide_and_narrow_data
    """
    split = lambda s: re.split(unescape_backslash(delimiter), s)
    standardised_lines = (split(line) for line in lines)

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
                        "timestamp": timestamp, "sensor": sensor, "reading": reading,
                    }


def insert(
    rows: typing.Iterable[str],
    columns: typing.Iterable[str],
    table: str,
    primary_key_columns: typing.Iterable[str],
) -> None:

    n_rows_to_insert = 10_000
    _uuid = secrets.token_hex(8)
    temp_table = f"{table}__temp__{_uuid}"

    msg = (
        "`primary_key_columns` must be defined"
        + " in order to skip duplicate values on copying from a file!"
    )
    assert primary_key_columns, msg
    primary_keys = ", ".join(primary_key_columns)

    try:
        with transaction.atomic():
            with closing(connection.cursor()) as cursor:

                cursor.execute(
                    f"""
                    create temp table {temp_table} (
                        like {table}
                    );
                    """
                )

                cursor.copy_from(
                    file=StringIteratorIO(row for row in rows),
                    table=temp_table,
                    columns=columns,
                    sep=',',
                    null="NULL"
                )

                cursor.execute(f"select count(*) from {temp_table}")
                result = cursor.fetchone()
                table_size = result[0]
                assert table_size > 0, f"No readings found in file!"

                for offset in range(0, table_size, n_rows_to_insert):
                    percentage_complete = round(100 * offset / table_size, 2)
                    cursor.execute(
                        f"""
                        -- {percentage_complete}%
                        with chunk as (
                            select *
                            from {temp_table}
                            limit {n_rows_to_insert}
                            offset {offset}
                        )
                                insert into {table}
                            select distinct on ({primary_keys}) *
                                    from chunk;
                        """
                    )

                cursor.execute(
                    f"""
                    drop table {temp_table}
                    """
                )

    except Exception as e:
        raise ValidationError(f"File parsing failed  | Error: {e})") from e


def import_to_db(
    file_obj,
) -> None:

    target_table = "sensor_reading_generic"

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

        with file_obj.file.open(encoding=file_obj.type.encoding) as f:
            rows = yield_readings(
                lines=f,
                encoding=file_obj.type.encoding,
                delimiter=file_obj.type.delimiter,
                datetime_fieldnames=file_obj.type.datetime_fieldnames,
                datetime_formats=file_obj.type.datetime_formats,
                na_values=file_obj.type.na_values,
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
