# Generated by Django 5.0.7 on 2024-07-28 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tariff', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tariff',
            name='type',
            field=models.CharField(choices=[('WATER', 'Вода'), ('MAINTENANCE', 'Содержание имущества')], max_length=30, unique=True, verbose_name='тип тарифа'),
        ),
    ]
