
from django.urls import path

from .views import deleteCity, index

urlpatterns = [
    path("", index, name="home"),
    path("delete/<int:city_id>", deleteCity, name="delete"),
]
