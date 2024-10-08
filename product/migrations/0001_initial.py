# Generated by Django 4.0.3 on 2022-05-20 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BasketStatus',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('status', models.CharField(
                    choices=[('Оплачено', 'Оплачено'),
                             ('Не оплачено', 'Не оплачено')],
                    default='Не оплачено', max_length=20,
                    verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('phone_number', models.PositiveSmallIntegerField(
                    verbose_name='Номер телефона')),
                ('comment', models.TextField(
                    blank=True, max_length=3000, null=True,
                    verbose_name='Комментарий')),
                ('telegram_user_id', models.PositiveSmallIntegerField(
                    verbose_name='Telegram Id пользователя')),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('status', models.CharField(
                    choices=[('Новый', 'Новый'), ('В процессе', 'В процессе'),
                             ('Выполнено', 'Выполнено')], default='Новый',
                    max_length=20, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentWay',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('payment_way', models.CharField(
                    choices=[('Наличные', 'Наличные'), ('Карта', 'Карта')],
                    default='Наличные', max_length=20,
                    verbose_name='Способ оплаты')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('review', models.TextField(max_length=5000)),
                ('order_id', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='reviews', to='product.order',
                    verbose_name='Id заказа')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(
                    auto_now_add=True, verbose_name='Время создания')),
                ('is_deleted', models.BooleanField(default=False)),
                ('product_name', models.CharField(
                    max_length=200, verbose_name='Название блюда')),
                ('photo', models.ImageField(
                    blank=True, null=True, upload_to='menu_photo',
                    verbose_name='Фото блюда')),
                ('description', models.TextField(
                    blank=True, max_length=3000, null=True,
                    verbose_name='Описание блюда')),
                ('price', models.PositiveIntegerField(
                    default=0, verbose_name='Цена')),
                ('available', models.CharField(
                    choices=[('Есть', 'есть'), ('Нет', 'нет')],
                    default='есть', max_length=20, verbose_name='наличие')),
                ('category', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='products', to='product.category')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'permissions': [('can_use_it', 'Можно использовать это')],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='payment_way',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='orders', to='product.paymentway',
                verbose_name='Способ оплаты'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='orders', to='product.orderstatus',
                verbose_name='Статус'),
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('telegram_user_id', models.PositiveSmallIntegerField(
                    verbose_name='Telegram Id пользователя')),
                ('amount', models.PositiveSmallIntegerField(
                    verbose_name='Количество')),
                ('product_total_price', models.PositiveIntegerField(
                    blank=True, null=True,
                    verbose_name='Цена блюда * на количество')),
                ('product', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='baskets', to='product.product',
                    verbose_name='Блюдо')),
                ('status', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='baskets', to='product.basketstatus',
                    verbose_name='Статус')),
            ],
        ),
    ]
