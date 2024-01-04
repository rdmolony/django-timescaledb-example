import textwrap

from django.contrib.postgres.fields import ArrayField
from django.db import models


class FileType(models.Model):
    name = models.CharField(max_length=50)
    na_values = ArrayField(
        base_field=models.CharField(max_length=10),
        default=["NaN"],
        help_text=textwrap.dedent(
            r"""A list of strings to recognise as empty values. <br>
            
            Default: ["NaN"] <br>

            Note: "" is also included by default <br>

            Example: ["NAN", "-9999", "-9999.0"]
            """
        ),
    )
    delimiter = models.CharField(
        max_length=5,
        help_text=textwrap.dedent(
            r"""The character used to separate fields in the file. <br>
            
            Default: "," <br>
            
            Examples: "," or ";" or "\s+" for whitespace or "\t" for tabs
            """
        ),
        default=",",
    )
    datetime_fieldnames = ArrayField(
        base_field=models.CharField(max_length=50),
        default=["Tmstamp"],
        help_text=textwrap.dedent(
            r"""A list of datetime field names. <br>
            
            Examples: <br>
            
            1) Data has a single datetime field named "Tmstamp" which has values like
            '2021-06-29 00:00:00.000':  ["Tmstamp"] <br>

            2) Data has two datetime fields named "Date" and "Time" which have values
            like '01.01.1999' and '00:00' respectively: ["Date","Time"] <br>
            """
        ),
    )
    encoding = models.CharField(
        max_length=25,
        help_text=textwrap.dedent(
            r"""The encoding of the file. <br>

            Default: "utf-8" <br>

            Examples: utf-8 or latin-1 or cp1252
            """
        ),
        default="utf-8",
    )
    datetime_formats = ArrayField(
        base_field=models.CharField(max_length=25),
        help_text=textwrap.dedent(
            r"""The datetime format of `datetime_columns`. <br>

            See https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
            for format codes

            Default: "%Y-%m-%d %H:%M:%S" <br>

            Examples: "%Y-%m-%d %H:%M:%S" for "2021-03-01 00:00:00"
            """
        ),
        default=[r"%Y-%m-%d %H:%M:%S"],
    )


class File(models.Model):
    file = models.FileField(upload_to="readings/", blank=False, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey(FileType, on_delete=models.RESTRICT)


class Reading(models.Model):
    timestamp = models.DateTimeField(blank=False, null=False, primary_key=True)
    sensor_name = models.TextField(blank=False, null=False)
    reading = models.TextField(blank=False, null=False)

    class Meta:
        managed = False
