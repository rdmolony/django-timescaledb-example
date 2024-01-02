from django.db import models


class File(models.Model):
    file = models.FileField(upload_to="readings/", blank=False, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Reading(models.Model):
    timestamp = models.DateTimeField(blank=False, null=False)
    sensor_name = models.TextField(blank=False, null=False)
    reading = models.FloatField(blank=False, null=False)

    class Meta:
        managed = False
