from django.contrib import admin
from .models import DataEntry, HealthReport

@admin.register(DataEntry)
class AdminDataEntry(admin.ModelAdmin):
    list_display = ["id", "name", "heart_rate", "blood_pressure", "sleep_duration", "oxygen_saturation", "body_temperature", "bmi"]
    search_fields = ["name"]
    list_filter = ["blood_pressure"]

@admin.register(HealthReport)
class AdminHealthReport(admin.ModelAdmin):
    list_display = ["id", "data_entry", "status"]
    search_fields = ["status"]
    list_filter = ["status"]
