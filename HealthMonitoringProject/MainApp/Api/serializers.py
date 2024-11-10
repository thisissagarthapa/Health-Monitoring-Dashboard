from MainApp.models import DataEntry
from rest_framework import serializers

class DataEntrySerializers(serializers.ModelSerializer):
    class Meta:
        model=DataEntry
        fields='__all__'