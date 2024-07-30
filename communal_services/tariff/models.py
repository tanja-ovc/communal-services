from django.db import models


class TariffType(models.TextChoices):
    WATER = 'WATER', 'Вода'
    MAINTENANCE = 'MAINTENANCE', 'Содержание имущества'


class Tariff(models.Model):
    type = models.CharField(
        'тип тарифа',
        choices=TariffType.choices,
        max_length=30,
        unique=True
    )
    rate = models.FloatField(
        'стоимость по тарифу',
    )

    def __str__(self):
        return f'Тариф "{self.type}"'

    def calculate_total_charge(self, multiplier):
        return self.rate * multiplier
