# views.py

from rest_framework import viewsets, status
from .serializers import DataEntrySerializers
from MainApp.models import DataEntry
from rest_framework.response import Response

class DataEntryView(viewsets.ModelViewSet):
    queryset = DataEntry.objects.all()
    serializer_class = DataEntrySerializers
    
    def create(self, request, *args, **kwargs):
        # Pass 'many=True' if expecting a list of data
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
