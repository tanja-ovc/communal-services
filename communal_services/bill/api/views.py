from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from bill.api.serializers import CalculationProgressSerializer
from bill.models import CalculationProgress
from bill.tasks import monthly_bill_calculation


@api_view(['POST'])
def start_monthly_bill_calculation(request, building_id):

    month_year = request.query_params.get('month_year')

    monthly_bill_calculation.delay(building_id, month_year)

    return Response(
        {'detail': 'Вычисление квартплат по дому запущено.'},
        status.HTTP_200_OK
    )


@api_view(['GET'])
def get_calculation_progress(request, building_id):
    month_year = request.query_params.get('month_year')

    building = CalculationProgress.objects.get(
        building_id=building_id, month_year=month_year
    )

    serializer = CalculationProgressSerializer(building, many=False)

    return Response(data=serializer.data, status=status.HTTP_200_OK)
