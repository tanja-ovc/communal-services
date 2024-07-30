from rest_framework import serializers

from bill.models import CalculationProgress, MonthlyBill


class CalculationProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculationProgress
        fields = (
            'id',
            'building',
            'month_year',
            'total_apartments',
            'completed_apartments',
            'completion_percentage',
            'status'
        )


class MonthlyBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyBill
        fields = (
            'id',
            'month_year',
            'water_supply_bill',
            'maintenance_bill',
            'total_bill',
        )
