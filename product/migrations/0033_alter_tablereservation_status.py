# Generated by Django 4.0.3 on 2022-06-20 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0032_alter_tablereservation_persons_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablereservation',
            name='status',
            field=models.CharField(choices=[('Новый', 'Новый'), ('Выполнено', 'Выполнено')], default='Новый', max_length=20, verbose_name='Статус'),
        ),
    ]
