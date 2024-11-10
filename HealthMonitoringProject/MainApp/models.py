from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class DataEntry(models.Model):
    name = models.CharField(max_length=50)
    heart_rate = models.IntegerField()  # typically beats per minute (bpm)
    blood_pressure = models.FloatField()  # assuming systolic (top number) only
    sleep_duration = models.FloatField()  # hours of sleep
    oxygen_saturation = models.FloatField()  # percentage
    body_temperature = models.FloatField()  # temperature in Celsius
    bmi = models.FloatField()  # body mass index
    created_at = models.DateTimeField(default=timezone.now)  # Set default to current time

    def __str__(self):
        return f"Data Entry {self.id} - {self.name}"



class HealthReport(models.Model):
    data_entry = models.ForeignKey(DataEntry, on_delete=models.CASCADE, related_name="health_reports")
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)  # Set default to current time

    def __str__(self):
        return f"{self.data_entry.name} - {self.status}"

