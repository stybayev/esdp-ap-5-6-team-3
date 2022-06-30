from pytest import fixture

from product.models import Category, ShoppingCartOrder, StatusShoppingCartOrder


@fixture
def category() -> Category:
    return Category.objects.create(
        category_name='Напитки',
        translit_category_name='Napitki',
        category_name_translation='Beverages'
    )


@fixture
def order_status() -> StatusShoppingCartOrder:
    return StatusShoppingCartOrder.objects.create(status='Новый')


@fixture
def order() -> ShoppingCartOrder:
    return ShoppingCartOrder.objects.create(
        telegram_user_id_id='965045582',
        status=order_status
    )
