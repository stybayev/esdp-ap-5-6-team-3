# Generated by Django 4.0.3 on 2022-06-24 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0040_alter_tablereservation_table_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablereservation',
            name='table_number',
            field=models.CharField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20)], max_length=20, null=True, verbose_name='Номер столика'),
        ),
    ]
