# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DataEntryView

# Set up router and register the viewset
router = DefaultRouter()
router.register('datahistory', DataEntryView, basename="datahistory")

# Define URL patterns
urlpatterns = [
    path('api/', include(router.urls)),
]
