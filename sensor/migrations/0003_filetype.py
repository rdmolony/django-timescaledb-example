# Generated by Django 5.0 on 2024-01-04 12:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0002_sensor_reading'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('na_values', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10), default=['NaN'], help_text='A list of strings to recognise as empty values. <br>\n\n            Default: ["NaN"] <br>\n\n            Note: "" is also included by default <br>\n\n            Example: ["NAN", "-9999", "-9999.0"]\n', size=None)),
                ('delimiter', models.CharField(default=',', help_text='The character used to separate fields in the file. <br>\n\n            Default: "," <br>\n\n            Examples: "," or ";" or "\\s+" for whitespace or "\\t" for tabs\n', max_length=5)),
                ('datetime_fieldnames', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), default=['Tmstamp'], help_text='A list of datetime field names. <br>\n\n            Examples: <br>\n\n            1) Data has a single datetime field named "Tmstamp" which has values like\n            \'2021-06-29 00:00:00.000\':  ["Tmstamp"] <br>\n\n            2) Data has two datetime fields named "Date" and "Time" which have values\n            like \'01.01.1999\' and \'00:00\' respectively: ["Date","Time"] <br>\n', size=None)),
                ('encoding', models.CharField(default='utf-8', help_text='The encoding of the file. <br>\n\n            Default: "utf-8" <br>\n\n            Examples: utf-8 or latin-1 or cp1252\n', max_length=25)),
                ('datetime_formats', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=25), default=['%Y-%m-%d %H:%M:%S'], help_text='The datetime format of `datetime_columns`. <br>\n\n            See https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes\n            for format codes\n\n            Default: "%Y-%m-%d %H:%M:%S" <br>\n\n            Examples: "%Y-%m-%d %H:%M:%S" for "2021-03-01 00:00:00"\n', size=None)),
            ],
        ),
    ]
