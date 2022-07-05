import pytest

from product.services import (category_create, aboutus_create,
                              product_create, order_change_status,
                              table_reservation_accept, cancel_order)


@pytest.mark.django_db
def test_category_create():
    category_record = {
        'category_name': 'Напитки',
        'translit_category_name': 'Napitki',
        'category_name_translation': 'Beverages'
    }
    assert category_create(category_record)


@pytest.mark.django_db
def test_aboutus_create():
    aboutus_record = {
        'description': 'Что-то о компании',
        'telephone_number': '84563217896'
    }
    assert aboutus_create(aboutus_record)


@pytest.mark.django_db
def test_product_create(category):
    product_record = {
        'product_name': 'Фанта',
        'description': 'выаываыа',
        'available': 'Есть',
        'price': '250'
    }
    product_photo = {
        'photo': 'sword-art-online-asuna-yuuki-5330.jpg',
    }
    assert product_create(product_record, product_photo, category)


@pytest.mark.django_db
def test_order_change_status(order, order_status):
    order_record = {
        'status': order_status,
        'telegram_user_id': '965045582'
    }
    assert order_change_status(order_record, order)


@pytest.mark.django_db
def test_order_cancel_status(order):
    order_record = {
        'telegram_user_id': '965045582'
    }
    assert cancel_order(order_record, order)


@pytest.mark.django_db
def test_table_reservation_accept(table_reservation):
    table_reservation_record = {
        'table_number': '1'
    }
    assert table_reservation_accept(table_reservation_record,
                                    table_reservation)
