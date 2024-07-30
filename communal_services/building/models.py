from django.db import models


class Building(models.Model):
    address = models.CharField(
        'адрес',
        max_length=350
    )

    def __str__(self):
        return f'Дом по адресу {self.address}'


class Apartment(models.Model):
    number = models.IntegerField('номер')
    floor_area = models.FloatField(
        'площадь',
        help_text='в кв. м.'
    )
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='apartments',
        verbose_name='квартира'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['number', 'building'],
                name='unique_apartment_number_in_building'
            )
        ]

    def __str__(self):
        return f'Квартира № {self.number} в доме по адресу {self.building.address}'
