from datetime import datetime, timedelta

from django.db import models

from building.models import Apartment


class MeterType(models.TextChoices):
    WATER = 'WATER', 'Вода'


class Meter(models.Model):
    type = models.CharField(
        'тип счётчика',
        choices=MeterType.choices,
        max_length=20
    )
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='meters',
        verbose_name='счётчик'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['type', 'apartment'],
                name='unique_meter_type_for_one_apartment'
            )
        ]

    def __str__(self):
        return f'Счётчик "{self.type}"'


class MeterReadings(models.Model):
    meter = models.ForeignKey(
        Meter,
        on_delete=models.CASCADE,
        related_name='readings',
        verbose_name='показания'
    )
    month_year = models.CharField(
        'месяц и год',
        max_length=6,
        help_text='ММГГГГ'
    )
    readings = models.IntegerField(
        'показания'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['meter', 'month_year'],
                name='unique_monthly_meter_readings_for_one_apartment'
            )
        ]

    def __str__(self):
        return f'Показания счётчика "{self.meter.type}" за {self.month_year}.'

    @property
    def passed_month_consumption(self):
        current_month = self.month_year
        current_month_date = datetime.strptime(current_month, '%m%Y')
        first_day_current_month = current_month_date.replace(day=1)
        last_day_passed_month = first_day_current_month - timedelta(days=1)
        passed_month = last_day_passed_month.strftime('%m%Y')
        passed_month_readings = MeterReadings.objects.get(
            meter=self.meter, month_year=passed_month
        )
        passed_month_consumption = self.readings - passed_month_readings.readings
        return passed_month_consumption
