# sensors/urls.py
from django.urls import path
from .views import get_all, create_data, get_last

urlpatterns = [
    path("sensors/", get_all, name="list_sensors"),
    path("sensors/add/", create_data, name="create_sensor"),
    path("sensors/last/", get_last, name="last_sensor"),
]
