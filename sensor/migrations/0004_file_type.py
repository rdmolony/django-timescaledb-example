# Generated by Django 5.0 on 2024-01-04 12:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0003_filetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, to='sensor.filetype'),
            preserve_default=False,
        ),
    ]
