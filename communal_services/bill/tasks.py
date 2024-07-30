import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.transaction import atomic

from bill.models import MonthlyBill, CalculationProgress, CalculationProgressStatus
from building.models import Apartment
from celery_app import app
from meter.models import MeterReadings
from tariff.models import Tariff

logger = logging.getLogger(__name__)


@app.task(queue='bills')
def monthly_bill_calculation(building_id, month_year):
    try:
        with atomic():
            logger.info(f'Месяц/год: {month_year}')

            apartments = Apartment.objects.filter(building_id=building_id).exclude(
                monthly_bills__month_year=month_year
            )
            logger.info(f'Список квартир: {apartments}')

            for apartment in apartments:
                logger.info(f'Квартира: {apartment}')

                water_supply_tariff = Tariff.objects.get(type='WATER')

                water_meter_readings = MeterReadings.objects.get(
                    meter__type='WATER',
                    meter__apartment_id=apartment.id,
                    month_year=month_year
                )
                passed_month_water_consumption = water_meter_readings.passed_month_consumption
                logger.info(f'Расход воды: {passed_month_water_consumption}')

                water_supply_bill = water_supply_tariff.calculate_total_charge(
                    passed_month_water_consumption
                )
                logger.info(f'Сумма за воду: {water_supply_bill}')

                maintenance_tariff = Tariff.objects.get(type='MAINTENANCE')

                maintenance_bill = maintenance_tariff.calculate_total_charge(
                    apartment.floor_area
                )
                logger.info(f'Сумма за maintenance: {maintenance_bill}')
                logger.info(f'Общая сумма счёта: {water_supply_bill + maintenance_bill}')

                bill = MonthlyBill.objects.create(apartment_id=apartment.id,
                                                  month_year=month_year,
                                                  water_supply_bill=water_supply_bill,
                                                  maintenance_bill=maintenance_bill,
                                                  total_bill=water_supply_bill + maintenance_bill)
                logger.info(f'{bill} создан.')

                add_to_calculation_progress.delay(building_id, month_year)

                logger.info(f'Созданный счёт будет учтён в прогрессе расчёта квартплаты по дому.')

    except ObjectDoesNotExist as e:
        logger.error(f'Объект не найден: {e}')
    except Exception as e:
        logger.error(f'Ошибка: {e}')


@app.task(queue='bills_progress')
def add_to_calculation_progress(building_id, month_year):
    try:
        with atomic():
            calculation_progress, created = CalculationProgress.objects.get_or_create(
                building_id=building_id,
                month_year=month_year,
            )
            logger.info(f'Счёт включается в расчёт...')

            calculation_progress.status = CalculationProgressStatus.IN_PROGRESS

            completed_apartments = MonthlyBill.objects.filter(
                apartment__building_id=building_id,
                month_year=month_year
            ).count()
            calculation_progress.completed_apartments = completed_apartments

            if calculation_progress.total_apartments == calculation_progress.completed_apartments:
                calculation_progress.status = CalculationProgressStatus.COMPLETED

            logger.info(f'Счёт включён в расчёт.')

            calculation_progress.save()

    except Exception as e:
        logger.error(f'Ошибка: {e}')
