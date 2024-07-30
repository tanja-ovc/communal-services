# Generated by Django 5.0.7 on 2024-07-27 15:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('building', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_year', models.CharField(help_text='ММГГГГ', max_length=6, verbose_name='месяц и год')),
                ('water_supply_bill', models.FloatField(default=0, verbose_name='счёт за воду')),
                ('maintenance_bill', models.FloatField(default=0, verbose_name='счёт за содержание имущества')),
                ('total_bill', models.FloatField(default=0, verbose_name='общий счёт')),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_bills', to='building.apartment', verbose_name='счёт за квартиру')),
            ],
        ),
    ]
