from django.urls import path

from bill.api.views import get_calculation_progress, start_monthly_bill_calculation

urlpatterns = [
    path('start_calculation/<int:building_id>/', start_monthly_bill_calculation),
    path('get_calculation_progress/<int:building_id>/', get_calculation_progress)
]
