from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.deletion import get_candidate_relations_to_delete
# from imagekit.models import ImageSpecField
# from pilkit.processors import Transpose, ResizeToFill


class CustomModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Entity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания", blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = CustomModelManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        delete_candidates = get_candidate_relations_to_delete(self.__class__._meta)
        if delete_candidates:
            for rel in delete_candidates:
                if rel.on_delete.__name__ == 'CASCADE' and rel.one_to_many and not rel.hidden:
                    for item in getattr(self, rel.related_name).all():
                        item.delete()
        self.save(update_fields=['is_deleted', ])

    class Meta:
        abstract = True


class Aboutus(models.Model):
    description = models.CharField(max_length=500, verbose_name="О Нас")
    telephone_number = models.PositiveIntegerField(verbose_name="Телефон компании")

    def __str__(self):
        return f"{self.description}"


class Category(models.Model):
    category_name = models.CharField(max_length=200, null=False, blank=False, verbose_name="Категория")
    translit_category_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Транслит Категория")
    category_name_translation = models.CharField(max_length=200, null=True, blank=True, verbose_name="Перевод Категория")

    def __str__(self):
        return self.category_name

    def get_products(self):
        return Product.objects.filter(category=self).values_list('category', flat=True)

    def products_count(self):
        return self.get_products().count()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(Entity):
    STATUS = [
        ('Есть', 'есть'),
        ('Нет', 'нет'),
    ]
    product_name = models.CharField(max_length=200, null=False, blank=False, verbose_name="Название блюда")
    category = models.ForeignKey('product.Category', on_delete=models.CASCADE,
                                 null=False, blank=False, related_name='products', verbose_name="Категория")
    photo = models.ImageField(upload_to='menu_photo',
                              verbose_name='Фото блюда',
                              )
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name="Описание блюда")
    price = models.PositiveIntegerField(null=False, blank=False, default=0, verbose_name="Цена")
    available = models.CharField(null=False, blank=False, choices=STATUS, verbose_name='наличие', default="есть",
                                 max_length=20)
    translit_product_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Транслитератор Название блюда")
    translit_description = models.TextField(max_length=3000, null=True, blank=True, verbose_name="Транслитератор Описание блюда")
    product_name_translation = models.CharField(max_length=200, null=True, blank=True, verbose_name="Перевод блюд")
    description_translation = models.CharField(max_length=3000, null=True, blank=True, verbose_name="Перевод описание блюд")

    def __str__(self):
        return f"{self.pk}. {self.product_name}. {self.category}. {self.price}"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        permissions = [
            ('can_use_it', 'Можно использовать это')
        ]


class BasketStatus(models.Model):
    PAID = 'Оплачено'
    NOTPAID = 'Не оплачено'

    STATUS = (
        (PAID, PAID), (NOTPAID, NOTPAID)
    )

    status = models.CharField(
        max_length=20, choices=STATUS, null=False, blank=False, default=NOTPAID, verbose_name="Статус"
    )

    def __str__(self):
        return self.status


class Basket(models.Model):
    PAID = 'Оплачено'
    NOTPAID = 'Не оплачено'

    STATUS = (
        (PAID, PAID), (NOTPAID, NOTPAID)
    )

    product = models.ForeignKey(
        'product.Product', on_delete=models.CASCADE, null=False, blank=False,
        related_name='baskets', verbose_name="Блюдо"
    )
    telegram_user_id = models.ForeignKey(
        'product.TelegramUser', on_delete=models.CASCADE, related_name='baskets_user', verbose_name="Телеграмм клиент"
    )
    amount = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name="Количество")
    product_total_price = models.PositiveIntegerField(null=True, blank=True, verbose_name="Цена блюда * на количество")
    status = models.CharField(
        max_length=20, choices=STATUS, null=False, blank=False, default=NOTPAID, verbose_name="Статус"
    )

    def __str__(self):
        return f"{self.product}. {self.telegram_user_id}. {self.amount}. {self.product_total_price}"


class BasketToOrder(models.Model):
    PAID = 'Оплачено'
    NOTPAID = 'Не оплачено'

    STATUS = (
        (PAID, PAID), (NOTPAID, NOTPAID)
    )

    product = models.ForeignKey(
        'product.Product', on_delete=models.CASCADE, null=False, blank=False,
        related_name='products', verbose_name="Блюдо"
    )
    telegram_user_id = models.ForeignKey(
        'product.TelegramUser', on_delete=models.CASCADE, related_name='baskets_users', verbose_name="Телеграмм клиент"
    )
    amount = models.PositiveSmallIntegerField(null=False, blank=False, verbose_name="Количество")
    product_total_price = models.PositiveIntegerField(null=True, blank=True, verbose_name="Цена блюда * на количество")
    status = models.CharField(
        max_length=20, choices=STATUS, null=False, blank=False, default=NOTPAID, verbose_name="Статус"
    )
    order = models.ForeignKey(
        'product.ShoppingCartOrder', on_delete=models.CASCADE, related_name='basket_order', verbose_name='Id заказа',
        default=1
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания", blank=True)

    def __str__(self):
        return f"{self.product}. {self.telegram_user_id}. {self.amount}. {self.product_total_price}"


class StatusShoppingCartOrder(models.Model):
    NEW = 'Новый'
    IN_PROGRESS = 'В процессе'
    DONE = 'Выполнено'

    STATUS = (
        (NEW, NEW), (IN_PROGRESS, IN_PROGRESS), (DONE, DONE)
    )

    status = models.CharField(
        max_length=20, choices=STATUS, null=False, blank=False, default=NEW, verbose_name="Статус")


class ShoppingCartOrder(models.Model):
    # NEW = 'Новый'
    # IN_PROGRESS = 'В процессе'
    # DONE = 'Выполнено'
    #
    # STATUS = (
    #     (NEW, NEW), (IN_PROGRESS, IN_PROGRESS), (DONE, DONE)
    # )

    telegram_user_id = models.ForeignKey(
        'product.TelegramUser', on_delete=models.CASCADE, related_name='telegram_users',
        verbose_name="Telegram Id пользователя"
    )

    status = models.ForeignKey('product.StatusShoppingCartOrder', on_delete=models.PROTECT, null=False, blank=False)

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время изменения", blank=True)

    def __str__(self):
        return f"{self.telegram_user_id}. {self.status}"

    def sum_product_total_price(self):
        return sum(BasketToOrder.objects.filter(order=self).values_list('product_total_price', flat=True))

    def service_price(self):
        return (self.sum_product_total_price() * 10) / 100

    def total_sum(self):
        return self.service_price() + self.sum_product_total_price()


class ShoppingCartOrderBasketToOrder(models.Model):
    shopping_cart_order = models.ForeignKey(
        'product.ShoppingCartOrder', on_delete=models.PROTECT, related_name='shopping_cart_orders', verbose_name='Id заказа'
    )
    baske_to_order = models.ForeignKey(
        'product.BasketToOrder', on_delete=models.PROTECT, related_name='basket_to_orders', verbose_name='Id корзины'
    )


class Order(models.Model):
    NEW = 'Новый'
    IN_PROGRESS = 'В процессе'
    DONE = 'Выполнено'

    STATUS = (
        (NEW, NEW), (IN_PROGRESS, IN_PROGRESS), (DONE, DONE)
    )

    CASH = 'Наличные'
    CARD = 'Карта'

    PAYMENT_WAY = (
        (CASH, CASH), (CARD, CARD)
    )

    phone_number = models.PositiveSmallIntegerField(blank=False, null=False, verbose_name="Номер телефона")
    comment = models.TextField(max_length=3000, null=True, blank=True, verbose_name="Комментарий")
    telegram_user_id = models.PositiveSmallIntegerField(
        null=False, blank=False, verbose_name="Telegram Id пользователя"
    )
    status = models.CharField(
        max_length=20, choices=STATUS, null=False, blank=False, default=NEW, verbose_name="Статус"
    )
    payment_way = models.CharField(
        max_length=20, choices=PAYMENT_WAY, null=False, blank=False, default=CASH, verbose_name="Способ оплаты"
    )
    basket_id = models.ForeignKey(
        'product.Basket', on_delete=models.PROTECT, null=True, blank=True,
        related_name='orders', verbose_name='Id корзины'
    )

    def __str__(self):
        return f"{self.phone_number}. {self.comment}. {self.telegram_user_id}. {self.status}. {self.payment_way}"


class Review(models.Model):
    review = models.TextField(max_length=5000, null=False, blank=False)
    order_id = models.ForeignKey(
        'product.Order', on_delete=models.CASCADE, null=False, blank=False,
        related_name='reviews', verbose_name="Id заказа"
    )

    def __str__(self):
        return f"{self.review}. {self.order_id}"


class TelegramUser(models.Model):
    user_id = models.PositiveSmallIntegerField(primary_key=True, unique=True, verbose_name="Telegram Id пользователя")
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Фамилия")
    phone_number = models.PositiveSmallIntegerField(verbose_name="Телефон")
    vcard = models.CharField(max_length=300, null=True, blank=True, verbose_name="Электронная карта")


class MerchantTelegramUser(models.Model):
    user_id = models.PositiveSmallIntegerField(primary_key=True, unique=True, verbose_name="Telegram Id пользователя")
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Фамилия")
    phone_number = models.PositiveSmallIntegerField(verbose_name="Телефон")
    vcard = models.CharField(max_length=300, null=True, blank=True, verbose_name="Электронная карта")


class TableReservation(models.Model):
    NEW = 'Новый'
    DONE = 'Выполнено'

    STATUS = (
        (NEW, NEW), (DONE, DONE)
    )
    TABLE_NUMBERS = []
    for t in range(1, 21):
        TABLE_NUMBERS.append((t, t))

    status = models.CharField(
        max_length=20, choices=STATUS, null=False, blank=False, default=NEW, verbose_name="Статус"
    )
    telegram_user_id = models.PositiveSmallIntegerField(
        null=False, blank=False, verbose_name="Telegram Id пользователя"
    )
    date = models.DateField(
        null=False, blank=False, verbose_name="Дата бронирования"
    )
    time = models.TimeField(
        null=False, blank=False, verbose_name="Время бронирования"
    )
    persons_number = models.CharField(
        null=False, max_length=20, blank=False, verbose_name="Количество человек"
    )
    table_number = models.CharField(
        max_length=20,
        null=True, blank=True, choices=TABLE_NUMBERS, verbose_name="Номер столика"
    )

    def __str__(self):
        return f"{self.telegram_user_id} - {self.table_number}.{self.status}"
