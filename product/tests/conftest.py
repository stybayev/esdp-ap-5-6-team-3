from pytest import fixture

from product.models import (Category, ShoppingCartOrder,
                            StatusShoppingCartOrder,
                            TelegramUser, TableReservation)


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
def telegram_user_id() -> TelegramUser:
    return TelegramUser.objects.create(
        user_id='965045582',
        first_name='just',
        last_name='r',
        phone_number='87770918657'
    )


@fixture
def order(order_status, telegram_user_id) -> ShoppingCartOrder:
    return ShoppingCartOrder.objects.create(
        telegram_user_id=telegram_user_id,
        status=order_status
    )


@fixture
def table_reservation(telegram_user_id) -> TableReservation:
    return TableReservation.objects.create(
        telegram_user_id=telegram_user_id,
        date='2022-06-21',
        time='22:00:00',
        status='Новый',
        persons_number='6-10',
    )
