from django.db import models

# Create your models here.
class Reading(models.Model):
    timestamp = models.DateTimeField(blank=False, null=False)
    sensor_name = models.TextField(blank=False, null=False)
    reading = models.FloatField(blank=False, null=False)

    class Meta:
        managed = False
