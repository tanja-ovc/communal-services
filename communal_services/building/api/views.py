import logging

from django.db.models import Prefetch
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from building.api.serializers import BuildingSerializer
from building.models import Apartment, Building
from meter.models import Meter

logger = logging.getLogger(__name__)


@api_view(['POST'])
def create_building(request):
    serializer = BuildingSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def read_building(request, building_id):
    building = Building.objects.filter(id=building_id).prefetch_related(
            Prefetch('apartments', queryset=Apartment.objects.prefetch_related(
                'monthly_bills',
                Prefetch('meters', queryset=Meter.objects.prefetch_related('readings'))
                ),
            ),
        ).first()
    serializer = BuildingSerializer(building, many=False)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
