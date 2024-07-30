# Generated by Django 5.0.7 on 2024-07-28 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0002_alter_apartment_floor_area_and_more'),
        ('meter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meter',
            name='type',
            field=models.CharField(choices=[('WATER', 'Вода')], max_length=20, verbose_name='тип счётчика'),
        ),
        migrations.AddConstraint(
            model_name='meter',
            constraint=models.UniqueConstraint(fields=('type', 'apartment'), name='unique_meter_type_for_one_apartment'),
        ),
        migrations.AddConstraint(
            model_name='meterreadings',
            constraint=models.UniqueConstraint(fields=('meter', 'month_year'), name='unique_monthly_meter_readings_for_one_apartment'),
        ),
    ]
