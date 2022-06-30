from pytest import fixture

from product.models import Category


@fixture
def category() -> Category:
    return Category.objects.create(
        category_name='Напитки',
        translit_category_name='Napitki',
        category_name_translation='Beverages'
    )