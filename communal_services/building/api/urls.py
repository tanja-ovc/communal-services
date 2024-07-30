from django.urls import path

from building.api.views import create_building, read_building

urlpatterns = [
    path('create/', create_building),
    path('read/<int:building_id>/', read_building)
]
