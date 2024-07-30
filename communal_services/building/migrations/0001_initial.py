# Generated by Django 5.0.7 on 2024-07-27 15:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=350, verbose_name='адрес')),
            ],
        ),
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='номер')),
                ('floor_area', models.FloatField(verbose_name='площадь')),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apartments', to='building.building', verbose_name='квартира')),
            ],
        ),
    ]