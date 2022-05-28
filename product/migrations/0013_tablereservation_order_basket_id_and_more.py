# Generated by Django 4.0.2 on 2022-05-28 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_category_category_name_translation_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_user_id', models.PositiveSmallIntegerField(verbose_name='Telegram Id пользователя')),
                ('date_n_time', models.DateTimeField(verbose_name='Дата и время бронирования')),
                ('persons_number', models.PositiveSmallIntegerField(verbose_name='Количество человек')),
                ('table_number', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Номер столика')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='basket_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='product.basket', verbose_name='Id корзины'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_way',
            field=models.CharField(choices=[('Наличные', 'Наличные'), ('Карта', 'Карта')], default='Наличные', max_length=20, verbose_name='Способ оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Новый', 'Новый'), ('В процессе', 'В процессе'), ('Выполнено', 'Выполнено')], default='Новый', max_length=20, verbose_name='Статус'),
        ),
        migrations.DeleteModel(
            name='OrderStatus',
        ),
        migrations.DeleteModel(
            name='PaymentWay',
        ),
    ]
