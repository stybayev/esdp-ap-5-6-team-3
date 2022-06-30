from product.models import Category, Aboutus
from transliterate import translit
from googletrans import Translator

translator = Translator()


def cyrillic_check(text):
    lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return lower.intersection(text.lower()) != set()


def category_create(data: dict) -> Category:
    category = Category.objects.create(category_name=data.get('category_name'))
    if cyrillic_check(category.category_name) is True:
        category.translit_category_name = translit(
            category.category_name, language_code='ru', reversed=True)
        category.category_name_translation = translator.translate(
            category.category_name, src='ru', dest='en').text
    else:
        category.translit_category_name = translit(
            category.category_name, 'ru')
        category.category_name_translation = translator.translate(
            category.category_name, src='en', dest='ru').text
    category.save()
    return category


def aboutus_create(data: dict) -> Aboutus:
    pass