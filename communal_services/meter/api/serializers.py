from rest_framework import serializers

from meter.models import Meter, MeterReadings


class MeterReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeterReadings
        fields = (
            'id',
            'month_year',
            'readings',
        )


class MeterSerializer(serializers.ModelSerializer):
    readings = MeterReadingsSerializer(many=True)

    class Meta:
        model = Meter
        fields = (
            'id',
            'type',
            'readings',
        )
