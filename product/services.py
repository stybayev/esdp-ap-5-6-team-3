from product.models import (Category, Aboutus,
                            Product, ShoppingCartOrder,
                            StatusShoppingCartOrder,
                            TableReservation, Basket,
                            CustomerFeedback, Comments)
from transliterate import translit
from googletrans import Translator
from transliterate import get_translit_function
from telebot import types
import telebot
from config import client_key
from django.contrib.auth.models import User

translator = Translator()
bot = telebot.TeleBot(client_key)


def cyrillic_check(text):
    """
        Функция для проверки текста на кириллица. Возвращает булевое значение.
    """
    lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return lower.intersection(text.lower()) != set()


def category_create(data: dict) -> Category:
    """
        Функция для создания записи 'Категории'.
        Возвращает запись созданной категории.
    """
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
    """
        Функция для создания записи 'О нас'
    """
    return Aboutus.objects.create(
        description=data.get('description'),
        telephone_number=data.get('telephone_number')
    )


def product_create(
        data: dict, files: dict,
        category: Category) -> Product:
    """
        Функция для создания записи 'Продукта'.
        Возвращает запись созданного продукта.
    """
    translit_ru = get_translit_function('ru')
    product = Product.objects.create(
        product_name=data.get('product_name'),
        category=category,
        description=data.get('description'),
        available=data.get('available'),
        price=data.get('price'),
        photo=files.get('photo')
    )
    if cyrillic_check(product.product_name) is True:
        product.translit_product_name = translit_ru(
            product.product_name, reversed=True)
        product.product_name_translation = translator.translate(
            product.product_name, src='ru', dest='en').text
    elif cyrillic_check(product.product_name) is False:
        product.translit_product_name = translit_ru(
            product.product_name)
        product.product_name_translation = translator.translate(
            product.product_name, src='en', dest='ru').text
    if cyrillic_check(product.description) is True:
        product.translit_description = translit_ru(
            product.description, reversed=True)
        product.description_translation = translator.translate(
            product.description, src='ru', dest='en').text
    elif cyrillic_check(product.description) is False:
        product.translit_description = translit_ru(product.description)
        if product.description:
            product.description_translation = translator.translate(
                product.description, src='en', dest='ru').text
    product.save()
    return product


def order_change_status(
        data_1: dict, order: ShoppingCartOrder) -> ShoppingCartOrder:
    """
        Функция для изменения статуса 'Заказа'. Возвращает
        запись заказа с измененным статусом.
    """
    current_status = data_1.get('status')
    telegram_user_id = data_1.get('telegram_user_id')
    statuses = StatusShoppingCartOrder.objects.all()
    for status in statuses:
        if status.status == current_status:
            order.status = status
            order.save()
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            detail_view_order = types.InlineKeyboardButton(
                text=f"Детальный просмотр заказа №{order.pk} \n",
                callback_data=f'order_detail_{order.pk}')
            keyboard.add(detail_view_order)
            if order.status_id == 2:
                bot.send_message(telegram_user_id,
                                 f"Заказ *№{order.pk}* "
                                 f"принята мерчантом в обработку \n ",
                                 reply_markup=keyboard,
                                 parse_mode='Markdown')
            elif order.status_id == 3:
                bot.send_message(telegram_user_id,
                                 f"Заказ *№{order.pk}* заверщен \n"
                                 f"Заказ перенесен в *Истории заказов*",
                                 parse_mode='Markdown')
    return order


def cancel_order(data_1: dict, order: ShoppingCartOrder) -> ShoppingCartOrder:
    """
        Функция для возврата 'Заказа'. Делает возврат удаления записи заказа.
    """
    telegram_user_id = data_1.get('telegram_user_id')
    for ord_bask in order.basket_order.all():
        basket = Basket.objects.create(
            product=ord_bask.product,
            telegram_user_id=ord_bask.telegram_user_id,
            amount=ord_bask.amount,
            product_total_price=ord_bask.product_total_price,
        )
        if basket.product.available == 'Нет':
            bot.send_message(telegram_user_id,
                             f"Заказ *№{order.pk}* "
                             f"возвращен в *Корзину* \n"
                             f"закончился *{basket.product.product_name}*",
                             parse_mode='Markdown')
        else:
            bot.send_message(telegram_user_id,
                             f"Заказ *№{order.pk}* "
                             f"возвращен в *Корзину* \n"
                             f"для уточнение просим обратиться к Мерчанту",
                             parse_mode='Markdown')
    return order.delete()


def table_reservation_accept(
        data_1: dict, reservation: TableReservation) -> TableReservation:
    """
        Функция для потверждения 'Брони столика'. Возвращает
        запись брони столика с измененным статусом.
    """
    reservation.status = 'Выполнено'
    reservation.table_number = data_1.get('table_number')
    bot.send_message(reservation.telegram_user_id_id,
                     f'Ваша бронь: Стол №{reservation.table_number}, '
                     f'дата: {reservation.date}, время:{reservation.time}',
                     parse_mode='Markdown')
    reservation.save()
    return reservation


# Пока неx работает. Описывать документацию к ней - не надо
def comment_create(data: dict, product: CustomerFeedback,
                   user: User) -> CustomerFeedback:
    comment = Comments.objects.create(text=data.get('text'))
    comment.feedback_id = product.pk
    comment.author = user
    comment.save()
    if product.description is not None:
        bot.send_message(
            product.telegram_user_id_id,
            f"_Оценка:{product.quiz_answer}, "
            f"{product.description}_ \n\n"
            f"*{comment.text}* \n ",
            parse_mode='Markdown')
    else:
        bot.send_message(
            product.telegram_user_id_id,
            f"_Оценка:{product.quiz_answer}, без отзыва_ \n\n"
            f"*{comment.text}* \n ",
            parse_mode='Markdown')
    return product
