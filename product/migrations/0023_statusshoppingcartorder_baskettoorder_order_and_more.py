# Generated by Django 4.0.3 on 2022-06-13 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product',
         '0022_merchanttelegramuser_remove_baskettoorder_order_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusShoppingCartOrder',
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
        migrations.AddField(
            model_name='baskettoorder',
            name='order',
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE,
                related_name='basket_order', to='product.shoppingcartorder',
                verbose_name='Id заказа'),
        ),
        migrations.AlterField(
            model_name='shoppingcartorder',
            name='status',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to='product.statusshoppingcartorder'),
        ),
    ]
