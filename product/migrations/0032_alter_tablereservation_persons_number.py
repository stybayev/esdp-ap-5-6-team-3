# Generated by Django 4.0.3 on 2022-06-20 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0031_alter_tablereservation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablereservation',
            name='persons_number',
            field=models.CharField(
                max_length=20, verbose_name='Количество человек'),
        ),
    ]
