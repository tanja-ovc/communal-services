from django.db.transaction import atomic
from rest_framework import serializers

from bill.api.serializers import MonthlyBillSerializer
from building.models import Apartment, Building
from meter.api.serializers import MeterSerializer


class ApartmentSerializer(serializers.ModelSerializer):
    meters = MeterSerializer(many=True, required=False)
    monthly_bills = MonthlyBillSerializer(many=True, required=False)

    class Meta:
        model = Apartment
        fields = (
            'id',
            'number',
            'floor_area',
            'meters',
            'monthly_bills',
        )


class BuildingSerializer(serializers.ModelSerializer):
    apartments = ApartmentSerializer(many=True)

    class Meta:
        model = Building
        fields = (
            'id',
            'address',
            'apartments',
        )

    @atomic
    def create(self, validated_data):
        apartments = validated_data.pop('apartments')
        building = Building.objects.create(**validated_data)
        apartment_objs = [Apartment(building_id=building.id, **apartment) for apartment in apartments]
        Apartment.objects.bulk_create(apartment_objs)
        return building
