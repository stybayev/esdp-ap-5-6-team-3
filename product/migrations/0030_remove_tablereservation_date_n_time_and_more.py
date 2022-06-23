# Generated by Django 4.0.3 on 2022-06-19 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_remove_tablereservation_condition_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tablereservation',
            name='date_n_time',
        ),
        migrations.AddField(
            model_name='tablereservation',
            name='date',
            field=models.DateField(
                default='2022-06-22', verbose_name='Дата бронирования'),
        ),
        migrations.AddField(
            model_name='tablereservation',
            name='time',
            field=models.TimeField(
                default='22:30', verbose_name='Время бронирования'),
        ),
    ]
