# Generated by Django 4.0.3 on 2022-06-27 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0046_alter_tablereservation_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablereservation',
            name='created_at',
            field=models.DateTimeField(blank=True, default='2022-06-02 08:55:20.064000', verbose_name='Время создания'),
        ),
    ]
