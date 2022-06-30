import pytest

from product.services import category_create


@pytest.mark.django_db
def test_category_create():
    category_post = {
        'category_name': 'Напитки',
        'translit_category_name': 'Napitki',
        'category_name_translation': 'Beverages'
    }

    assert category_create(category_post)
