from django.db import models

from building.models import Apartment, Building


class MonthlyBill(models.Model):
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='monthly_bills',
        verbose_name='счёт за квартиру'
    )
    month_year = models.CharField(
        'месяц и год',
        max_length=6,
        help_text='ММГГГГ'
    )
    water_supply_bill = models.FloatField(
        'счёт за воду',
        default=0
    )
    maintenance_bill = models.FloatField(
        'счёт за содержание имущества',
        default=0
    )
    total_bill = models.FloatField(
        'общий счёт',
        default=0
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['apartment', 'month_year'],
                name='unique_monthly_bill'
            )
        ]

    def __str__(self):
        return f'Счёт для квартиры №{self.apartment.number} за {self.month_year}'


class CalculationProgressStatus(models.TextChoices):
    PENDING = 'PENDING', 'не начат'
    IN_PROGRESS = 'IN_PROGRESS', 'в процессе'
    COMPLETED = 'COMPLETED', 'завершён'
    FAILED = 'FAILED', 'ошибка'


class CalculationProgress(models.Model):
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='calculation_progresses',
        verbose_name='дом'
    )
    month_year = models.CharField(
        'месяц и год',
        max_length=6,
        help_text='ММГГГГ'
    )
    completed_apartments = models.PositiveSmallIntegerField(
        'квартир обработано',
        default=0
    )
    status = models.CharField(
        'статус',
        choices=CalculationProgressStatus.choices,
        max_length=20,
        default=CalculationProgressStatus.PENDING
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['building', 'month_year'],
                name='unique_monthly_bill_calculation_progress'
            )
        ]

    @property
    def total_apartments(self):
        return self.building.apartments.count()

    @property
    def completion_percentage(self):
        return round((self.completed_apartments / self.total_apartments) * 100, 2)

    def __str__(self):
        return f'Расчёт квартплаты для дома по адресу {self.building.address}'
