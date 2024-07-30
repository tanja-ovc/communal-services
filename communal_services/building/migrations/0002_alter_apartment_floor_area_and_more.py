# Generated by Django 5.0.7 on 2024-07-28 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='floor_area',
            field=models.FloatField(help_text='в кв. м.', verbose_name='площадь'),
        ),
        migrations.AddConstraint(
            model_name='apartment',
            constraint=models.UniqueConstraint(fields=('number', 'building'), name='unique_apartment_number_in_building'),
        ),
    ]