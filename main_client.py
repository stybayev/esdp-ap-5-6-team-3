import datetime
import django
import os
from django.shortcuts import get_object_or_404
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()
import telebot
from telebot import types
from requests import get
from cal import Calendar, CallbackData, RUSSIAN_LANGUAGE, get_time, TIME, get_persons, PERSONS
from telebot.types import ReplyKeyboardRemove, CallbackQuery, InlineKeyboardMarkup
import time
from product.models import TelegramUser, Product, Basket, Aboutus, Category, BasketToOrder, ShoppingCartOrder, \
    ShoppingCartOrderBasketToOrder, StatusShoppingCartOrder, MerchantTelegramUser, TableReservation

merchant_key = '5474930369:AAFYwY-sfz8B8-mqT9b_oxhofE46UvBgpcA'
client_key = '5388600014:AAHFGhuoNaXEK7dcd-qRi0okx-Wa2S5Gs2U'
logger = telebot.logger
bot = telebot.TeleBot(client_key)
calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")
merchant_bot = telebot.TeleBot(merchant_key)

print(time.ctime())
time.sleep(3)

# # Для виртуального окружения
url_menu = 'http://localhost:8000/api/v1/menu/'
url_category = 'http://localhost:8000/api/v1/category/'

# Для docker-compose
# url_menu = 'http://localhost:8080/api/v1/menu/'
# url_category = 'http://localhost:8080/api/v1/category/'
database = {}

response_menu = get(url_menu).json()
response_categories = get(url_category).json()


def text_basket(basket):
    basket_text = (f"_Наименование_: *{basket.product.id}-{basket.product.product_name}* \n"
                   f"_Цена_: *{basket.product.price}* тенге \n"
                   f"_Категория_: *{basket.product.category}* \n"
                   f"_Описание_: *{basket.product.description}* \n\n"
                   f"_Количество_: *{basket.amount}* \n"
                   f"_Сумма_: {basket.product.price}x{basket.amount}= *{basket.product_total_price}* тенге \n")
    return basket_text


def text_menu(menu):
    menu_text = (f"_Наименование_: *{menu['id']}-{menu['product_name']}* \n"
                 f"_Цена_: *{menu['price']}* тенге \n"
                 f"_Категория_: *{menu['category']}* \n"
                 f"_Описание_: *{menu['description']}* \n")
    return menu_text


def subtract_meals(basket, menu):
    basket.amount -= 1
    basket.product_total_price -= menu['price']
    basket.save()


def add_meals(basket, menu):
    basket.amount += 1
    basket.product_total_price += menu['price']
    basket.save()


def button_basket(keyboard, basket):
    add_menu = types.InlineKeyboardButton(
        text=f"\U00002795\U0001F371Добавить в корзину",
        callback_data=f"add_basket_{basket.product.id}")
    subtract_menu = types.InlineKeyboardButton(
        text=f"\U00002796\U0001F371 удалить с корзины",
        callback_data=f"subtract_basket_{basket.product.id}")
    keyboard.add(add_menu, subtract_menu)


def button_menu(keyboard, basket):
    add_menu = types.InlineKeyboardButton(
        text=f"\U00002795\U0001F371Добавить в корзину",
        callback_data=f"add_menu_{basket.product.id}")
    subtract_menu = types.InlineKeyboardButton(
        text=f"\U00002796\U0001F371 удалить с корзины",
        callback_data=f"subtract_menu_{basket.product.id}")
    keyboard.add(add_menu, subtract_menu)


@bot.message_handler(commands=["start"])
def start(m):
    print(type(m.from_user.id))

    if TelegramUser.objects.filter(user_id=m.from_user.id):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg = bot.send_message(m.chat.id, f'Приветствую Вас *{m.from_user.first_name}*!', reply_markup=keyboard,
                               parse_mode="Markdown")
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                       ['\U0001F4D6\U0001F372\U0001F354Меню', '\U0001F371Корзина']])
        keyboard.add(
            *[types.KeyboardButton(bot_message) for bot_message in ['\U0001F4DCО Нас', '\U0001F45DОформить заказ']])
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                       ['\U0001F55CСтатус заказа', '\U0001F51AВыполненные заказы']])
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                       ['\U0001f6cb\ufe0fЗабронировать столик']])

        bot.send_message(m.chat.id, 'Выберите в меню операции!', reply_markup=keyboard)
        bot.register_next_step_handler(msg, bot_message)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text='\U0001F4F2Поделиться номером', request_contact=True))
        bot.send_message(m.chat.id, '\U0001F4F2Поделиться номером!', reply_markup=keyboard)


@bot.message_handler(content_types=["text", "contact"])
def bot_message(m):
    if m.contact is not None:
        TelegramUser.objects.get_or_create(user_id=m.contact.user_id, first_name=m.contact.first_name,
                                           last_name=m.contact.last_name, phone_number=m.contact.phone_number,
                                           vcard=m.contact.vcard)
        bot.send_message(m.chat.id, f'Пользователь *{m.contact.first_name} {m.contact.last_name} '
                                    f'{m.contact.phone_number}* добавлен в базу \U0001F4BB', parse_mode="Markdown")
        start(m)

    elif m.text == '\U0001F4D6\U0001F372\U0001F354Меню':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for response_category in response_categories:
            category = types.InlineKeyboardButton(
                text=f"{response_category['category_name']}-\U0001F355\U0001F354\U0001F379\U0001F382",
                callback_data=f"{response_category['category_name']}")

            keyboard.add(category)
        bot.send_message(m.chat.id, 'Категории\U0001F4C4\U0001F355\U0001F354\U0001F379\U0001F382',
                         reply_markup=keyboard, parse_mode="Markdown")

    elif m.text == '\U0001F4DCО Нас':
        for about in Aboutus.objects.all():
            bot.send_message(m.chat.id, f"*О НАС:* \n _{about.description}_ \n\n Телефон: *{about.telephone_number}*",
                             parse_mode="Markdown")

    elif m.text == '\U0001f6cb\ufe0fЗабронировать столик' or m.text == 'Изменить бронь':
        now = datetime.datetime.now()  # Получение сегодняшней даты
        bot.send_message(
            m.chat.id,
            "Выберите дату",
            reply_markup=calendar.create_calendar(
                name=calendar_1_callback.prefix,
                year=now.year,
                month=now.month,
            ),
        )
    elif m.text == 'Бронировать':
        TableReservation.objects.create(telegram_user_id=m.from_user.id,
                                        date=database[m.from_user.id]['date'], time=database[m.from_user.id]['time'],
                                        persons_number=database[m.from_user.id]['persons'])
        del database[m.from_user.id]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                       ['\U0001F4D6\U0001F372\U0001F354Меню', '\U0001F371Корзина']])
        keyboard.add(
            *[types.KeyboardButton(bot_message) for bot_message in ['\U0001F4DCО Нас', '\U0001F45DОформить заказ']])
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                       ['\U0001F55CСтатус заказа', '\U0001F51AВыполненные заказы']])
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                       ['\U0001f6cb\ufe0fЗабронировать столик']])
        bot.send_message(
            m.chat.id,
            "Вам придет ответа от менеджера",
            reply_markup=keyboard
            )
    elif m.text == '\U0001F371Корзина':
        for basket in Basket.objects.all():
            if m.from_user.id == basket.telegram_user_id_id:
                keyboard = types.InlineKeyboardMarkup(row_width=2)

                print(f"uploads/{basket.product.photo}")

                photo = open(f"uploads/{basket.product.photo}", 'rb')

                button_basket(keyboard, basket)
                bot.send_photo(m.chat.id, photo, caption=text_basket(basket), reply_markup=keyboard,
                               parse_mode="Markdown")
                # bot.export_chat_invite_link(m.chat.id)
                # print(bot.export_chat_invite_link(m.chat.id))
                # bot.forward_message(chat_id=m.chat.id, from_chat_id=m.chat.id, message_id=m.message_id)

        if not Basket.objects.filter(telegram_user_id_id=m.from_user.id):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(types.InlineKeyboardButton(text='\U0001F4D6\U0001F372\U0001F354Меню',
                                                    callback_data='\U0001F4D6\U0001F372\U0001F354Меню'))
            bot.send_message(m.chat.id,
                             '<i>Корзина пуста, перейдите в</i> <ins><b>Меню</b></ins> <i>для заказа блюд</i>',
                             reply_markup=keyboard, parse_mode="HTML")

    elif m.text == '\U0001F45DОформить заказ':
        if not Basket.objects.filter(telegram_user_id_id=m.from_user.id):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(types.InlineKeyboardButton(text='\U0001F4D6\U0001F372\U0001F354Меню',
                                                    callback_data='\U0001F4D6\U0001F372\U0001F354Меню'))
            bot.send_message(m.chat.id, f"_Заказ не можем создать, для начала выберите блюд из_ *Меню*  \n",
                             reply_markup=keyboard, parse_mode='Markdown')
        else:

            keyboard = types.InlineKeyboardMarkup(row_width=2)

            order_processing = types.InlineKeyboardButton(
                text=f"\U0001F45D Оформить заказ",
                callback_data=f"order_processing")
            change_basket = types.InlineKeyboardButton(
                text=f"\U0001F371 Изменить заказ - Корзина",
                callback_data="edit_basket")
            keyboard.add(order_processing, change_basket)

            total_sum = 0
            for basket in Basket.objects.all():
                if basket.telegram_user_id_id == m.from_user.id:
                    total_sum += basket.product_total_price
                    bot.send_message(m.chat.id, f"*{basket.product.product_name}:* *{basket.amount}*шт. *x* "
                                                f"*{basket.product.price}*тг. = *{basket.product_total_price}* тенге",
                                     parse_mode='Markdown')
            bot.send_message(m.chat.id, f"_Итого общая сумма продукта:_ *{total_sum}* \n"
                                        f"_10% за обслуживание:_ *{(total_sum * 10) / 100}* \n\n"
                                        f"Итого общая сумма: *{((total_sum * 10) / 100) + total_sum}*",
                             reply_markup=keyboard, parse_mode='Markdown')

    elif m.text == '\U0001F55CСтатус заказа':

        for orders in ShoppingCartOrder.objects.filter(telegram_user_id_id=m.from_user.id, status_id__lte=2):
            keyboard = types.InlineKeyboardMarkup(row_width=2)

            if orders.status_id == 1:
                detail_view_order = types.InlineKeyboardButton(
                    text=f"Детальный просмотр заказа №{orders.pk} \n",
                    callback_data=f'order_detail_{orders.pk}')
                keyboard.add(detail_view_order)
                bot.send_message(m.chat.id, f"Заказ *№{orders.id}* еще не принято,\n статус: *{orders.status.status}*",
                                 reply_markup=keyboard, parse_mode='Markdown')
            elif orders.status_id == 2:
                detail_view_order = types.InlineKeyboardButton(
                    text=f"Детальный просмотр заказа №{orders.pk}",
                    callback_data=f'order_detail_{orders.pk}')
                keyboard.add(detail_view_order)
                bot.send_message(m.chat.id,
                                 f"Заказ *№{orders.id}* принято в обработку,\n статус: *{orders.status.status}*",
                                 reply_markup=keyboard, parse_mode='Markdown')


def order(call):
    value = []
    for orders in ShoppingCartOrder.objects.filter(telegram_user_id_id=call.from_user.id, status_id__lte=2):
        value.append(f'order_detail_{orders.id}')
    return value


@bot.callback_query_handler(
    func=lambda call: call.data.startswith(calendar_1_callback.prefix)
)
def callback_inline(call: CallbackQuery):
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    global date
    date_in = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    database.setdefault(call.from_user.id, {'date': date_in.strftime('%Y-%m-%d')})
    if action == "DAY":
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"Выбранная дата: {database[call.from_user.id].get('date')}",
            reply_markup=ReplyKeyboardRemove(),
        )
        keyboard = InlineKeyboardMarkup(row_width=4)
        bot.send_message(
            chat_id=call.from_user.id,
            text="Выберите время",
            reply_markup=get_time(keyboard),
        )
    elif action == "ОТМЕНА":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Отменен",
            reply_markup=ReplyKeyboardRemove(),
        )


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data in order(call):
        order_pk = call.data[13:]
        total_sum = 0
        if BasketToOrder.objects.filter(telegram_user_id_id=call.from_user.id, order__status=1,
                                        order=order_pk):
            bot.send_message(call.message.chat.id, f"Заказ *№{order_pk}: еще не принято в обработку*",
                             parse_mode='Markdown')
        elif BasketToOrder.objects.filter(telegram_user_id_id=call.from_user.id, order__status=2,
                                          order=order_pk):
            bot.send_message(call.message.chat.id, f"Заказ *№{order_pk}: принято в обработку*", parse_mode='Markdown')
        for basket in BasketToOrder.objects.filter(telegram_user_id_id=call.from_user.id, order__status__lte=2,
                                                   order=order_pk):
            total_sum += basket.product_total_price
            bot.send_message(call.message.chat.id, f"_{basket.product.product_name}: {basket.amount}_шт. *x* "
                                                   f"_{basket.product.price}_тг. = _{basket.product_total_price}_ тенге",
                             parse_mode='Markdown')
        bot.send_message(call.message.chat.id, f"_Итого общая сумма продукта:_ *{total_sum}* \n"
                                               f"_10% за обслуживание:_ *{(total_sum * 10) / 100}* \n\n"
                                               f"Итого общая сумма: *{((total_sum * 10) / 100) + total_sum}*",
                         parse_mode='Markdown')
    if call.data in TIME:
        database[call.from_user.id]['time'] = call.data
        keyboard = InlineKeyboardMarkup(row_width=2)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Время: {call.data}",
            reply_markup=get_persons(keyboard)
        )
    if call.data in PERSONS:
        database[call.from_user.id]['persons'] = call.data
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                       ['Изменить бронь', 'Бронировать']])
        bot.send_message(
            chat_id=call.from_user.id,
            text=f'''Дата: {database[call.from_user.id]['date']}, время: {database[call.from_user.id]['time']}, количество людей: {database[call.from_user.id]['persons']}
            Изменить данные или продолжить?''',
            reply_markup=keyboard,
        )
    if call.data == 'order_processing':
        for status in StatusShoppingCartOrder.objects.all():
            if status.status == 'Новый':
                new_status = status
        shopping_cart_orders = ShoppingCartOrder.objects.create(
            telegram_user_id_id=call.from_user.id,
            status=new_status
        )
        total_sum = 0
        for menu in response_menu:

            for basket in Basket.objects.filter(telegram_user_id_id=call.from_user.id):
                if Basket.objects.filter(product_id=menu['id'], telegram_user_id_id=call.from_user.id):
                    basket_to_orders = BasketToOrder.objects.create(
                        product=basket.product,
                        telegram_user_id=basket.telegram_user_id,
                        amount=basket.amount,
                        product_total_price=basket.product_total_price,
                        status=basket.status,
                        order=shopping_cart_orders
                    )
                    basket.delete()
                    total_sum += basket.product_total_price

                    # ShoppingCartOrderBasketToOrder.objects.create(shopping_cart_order_id=shopping_cart_orders.pk,
                    #                                               baske_to_order_id=basket_to_orders.pk)

        bot.send_message(call.message.chat.id, f"*Заказ №{shopping_cart_orders.id} в обработке* \n"
                                               f"_Итого общая сумма продукта:_ *{total_sum}* \n"
                                               f"_10% за обслуживание:_ *{(total_sum * 10) / 100}* \n\n"
                                               f"Итого общая сумма: *{((total_sum * 10) / 100) + total_sum}*",
                         parse_mode='Markdown')
        for users in MerchantTelegramUser.objects.all():
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text=f"Перейти к заказу №{shopping_cart_orders.id}",
                                                    url=f"http://127.0.0.1:8000/order/{shopping_cart_orders.id}"))

            merchant_bot.send_message(users.user_id, f'поступил заказ с номером *№{shopping_cart_orders.id}* \n'
                                                     f'сумма заказа *{((total_sum * 10) / 100) + total_sum}* тенге',
                                      reply_markup=keyboard, parse_mode='Markdown')

    if call.data != '\U0001F4D6\U0001F372\U0001F354Меню':
        for menu in response_menu:

            if call.data == menu['category']:
                for response_category in response_categories:
                    # if Product.objects.filter(available='Есть', category_id=response_category['id']):
                    if menu['category'] == response_category['category_name'] and menu['available'] == 'Есть':
                        keyboard = types.InlineKeyboardMarkup(row_width=2)

                        print(menu['photo'][1:])

                        photo = open(menu['photo'][1:], 'rb')

                        if not Basket.objects.filter(product_id=menu['id'], telegram_user_id_id=call.from_user.id):
                            add_menu = types.InlineKeyboardButton(
                                text=f"\U00002795\U0001F371Добавить в корзину",
                                callback_data=f"add_menu_{menu['id']}")

                            keyboard.add(add_menu)

                            bot.send_photo(call.message.chat.id, photo, caption=text_menu(menu), reply_markup=keyboard,
                                           parse_mode="Markdown")

                        elif Basket.objects.filter(product_id=menu['id'], telegram_user_id_id=call.from_user.id):
                            basket = get_object_or_404(Basket, product_id=menu['id'],
                                                       telegram_user_id_id=call.from_user.id)

                            button_menu(keyboard, basket)

                            bot.send_photo(call.message.chat.id, photo, caption=text_basket(basket),
                                           reply_markup=keyboard,
                                           parse_mode="Markdown")

            elif call.data == f"add_menu_{menu['id']}":
                if not Basket.objects.filter(product_id=menu['id'], telegram_user_id_id=call.from_user.id):
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    basket = Basket.objects.create(
                        amount=1,
                        product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id,
                        product_total_price=menu['price'],
                    )

                    button_menu(keyboard, basket)

                    bot.edit_message_caption(caption=text_basket(basket), chat_id=call.message.chat.id,
                                             message_id=call.message.message_id,
                                             reply_markup=keyboard, parse_mode="Markdown")

                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text=f'"{basket.product.product_name}" добавлено в корзину \n Общая количество 1')

                elif Basket.objects.filter(product_id=menu['id'], telegram_user_id_id=call.from_user.id):
                    keyboard = types.InlineKeyboardMarkup(row_width=2)

                    basket = get_object_or_404(Basket, product_id=menu['id'], telegram_user_id_id=call.from_user.id)
                    add_meals(basket, menu)

                    button_menu(keyboard, basket)

                    bot.edit_message_caption(caption=text_basket(basket), chat_id=call.message.chat.id,
                                             message_id=call.message.message_id,
                                             reply_markup=keyboard, parse_mode="Markdown")
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text=f'"{basket.product.product_name}" добавлено в корзину \n Общая количество {basket.amount}')

            elif call.data == f"subtract_menu_{menu['id']}":
                for telegram_user in TelegramUser.objects.all():
                    if call.from_user.id == telegram_user.user_id:
                        if Basket.objects.filter(amount__gt=1, product_id=menu['id'],
                                                 telegram_user_id_id=telegram_user.user_id):
                            keyboard = types.InlineKeyboardMarkup(row_width=2)

                            basket = get_object_or_404(Basket, product_id=menu['id'],
                                                       telegram_user_id_id=telegram_user.user_id)

                            subtract_meals(basket, menu)

                            button_menu(keyboard, basket)
                            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                      text=f'"{basket.product.product_name}" удалено с корзины \n Общая количество {basket.amount}')
                            bot.edit_message_caption(caption=text_basket(basket), chat_id=call.message.chat.id,
                                                     message_id=call.message.message_id,
                                                     reply_markup=keyboard, parse_mode="Markdown")

                        elif Basket.objects.filter(amount=1, product_id=menu['id'],
                                                   telegram_user_id_id=telegram_user.user_id):
                            basket = Basket.objects.filter(amount=1, product_id=menu['id'],
                                                           telegram_user_id_id=call.from_user.id)
                            product = get_object_or_404(Basket, product_id=menu['id'],
                                                        telegram_user_id_id=telegram_user.user_id)
                            basket.delete()

                            keyboard = types.InlineKeyboardMarkup(row_width=2)
                            add_menu = types.InlineKeyboardButton(
                                text=f"\U00002795\U0001F371Добавить в корзину",
                                callback_data=f"add_menu_{menu['id']}")
                            keyboard.add(add_menu)
                            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                      text=f'"{product.product.product_name}" удалено с корзины')
                            bot.edit_message_caption(caption=text_menu(menu), chat_id=call.message.chat.id,
                                                     message_id=call.message.message_id,
                                                     reply_markup=keyboard, parse_mode="Markdown")

            elif call.data == f"add_basket_{menu['id']}":
                if not Basket.objects.filter(product_id=menu['id'], telegram_user_id_id=call.from_user.id):
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    basket = Basket.objects.create(
                        amount=1,
                        product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id,
                        product_total_price=menu['price'],
                    )
                    button_basket(keyboard, basket)

                    bot.edit_message_caption(caption=text_basket(basket), chat_id=call.message.chat.id,
                                             message_id=call.message.message_id,
                                             reply_markup=keyboard, parse_mode="Markdown")

                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text=f'"{basket.product.product_name}" добавлено в корзину \n Общая количество 1')

                elif Basket.objects.filter(product_id=menu['id'], telegram_user_id_id=call.from_user.id):
                    keyboard = types.InlineKeyboardMarkup(row_width=2)

                    basket = get_object_or_404(Basket, product_id=menu['id'], telegram_user_id_id=call.from_user.id)
                    add_meals(basket, menu)

                    button_basket(keyboard, basket)

                    bot.edit_message_caption(caption=text_basket(basket), chat_id=call.message.chat.id,
                                             message_id=call.message.message_id,
                                             reply_markup=keyboard, parse_mode="Markdown")
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text=f'"{basket.product.product_name}" добавлено в корзину \n Общая количество {basket.amount}')

            elif call.data == f"subtract_basket_{menu['id']}":
                if Basket.objects.filter(amount__gt=1, product_id=menu['id'], telegram_user_id_id=call.from_user.id):
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    basket = get_object_or_404(Basket, product_id=menu['id'], telegram_user_id_id=call.from_user.id)
                    subtract_meals(basket, menu)

                    button_basket(keyboard, basket)

                    bot.edit_message_caption(caption=text_basket(basket), chat_id=call.message.chat.id,
                                             message_id=call.message.message_id,
                                             reply_markup=keyboard, parse_mode="Markdown")
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text=f'"{basket.product.product_name}" удалено с корзины \n Общая количество {basket.amount}')

                elif Basket.objects.filter(amount=1, product_id=menu['id'], telegram_user_id_id=call.from_user.id):
                    basket = Basket.objects.filter(amount=1, product_id=menu['id'],
                                                   telegram_user_id_id=call.from_user.id)
                    product = get_object_or_404(Basket, product_id=menu['id'], telegram_user_id_id=call.from_user.id)
                    basket.delete()
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text=f'"{product.product.product_name}" удалено с корзины')
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id, timeout=1)
                    if not Basket.objects.filter(telegram_user_id_id=call.from_user.id):
                        keyboard = types.InlineKeyboardMarkup(row_width=1)
                        keyboard.add(types.InlineKeyboardButton(text='\U0001F4D6\U0001F372\U0001F354Меню',
                                                                callback_data='\U0001F4D6\U0001F372\U0001F354Меню'))
                        bot.send_message(call.message.chat.id, '_Корзина пуста, для добавление перейдите в_ *Меню* ',
                                         reply_markup=keyboard, parse_mode='Markdown')

            elif call.data == 'edit_basket':
                if Basket.objects.filter(product_id=menu['id'],
                                         telegram_user_id_id=call.from_user.id):  # call.from_user.id == basket.telegram_user_id_id:
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    basket = get_object_or_404(Basket, product_id=menu['id'], telegram_user_id_id=call.from_user.id)

                    print(f"uploads/{basket.product.photo}")

                    photo = open(f"uploads/{basket.product.photo}", 'rb')

                    button_basket(keyboard, basket)
                    bot.send_photo(call.message.chat.id, photo, caption=text_basket(basket), reply_markup=keyboard,
                                   parse_mode="Markdown")
                    # bot.export_chat_invite_link(m.chat.id)
                    # print(bot.export_chat_invite_link(m.chat.id))
                    # bot.forward_message(chat_id=m.chat.id, from_chat_id=m.chat.id, message_id=m.message_id)

                if not Basket.objects.filter(telegram_user_id_id=call.from_user.id):
                    keyboard = types.InlineKeyboardMarkup(row_width=1)
                    keyboard.add(types.InlineKeyboardButton(text='\U0001F4D6\U0001F372\U0001F354Меню',
                                                            callback_data='\U0001F4D6\U0001F372\U0001F354Меню'))
                    bot.send_message(call.message.chat.id,
                                     '<i>Корзина пуста, перейдите в</i> <ins><b>Меню</b></ins> <i>для заказа блюд</i>',
                                     reply_markup=keyboard, parse_mode="HTML")

    elif call.data == '\U0001F4D6\U0001F372\U0001F354Меню':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for api_category in response_categories:
            category = types.InlineKeyboardButton(
                text=f"{api_category['category_name']}-\U0001F355\U0001F354\U0001F379\U0001F382",
                callback_data=f"{api_category['category_name']}")
            keyboard.add(category)
        bot.send_message(call.message.chat.id, 'Категории\U0001F4C4\U0001F355\U0001F354\U0001F379\U0001F382',
                         reply_markup=keyboard, parse_mode="Markdown")


bot.polling(none_stop=True, interval=0)
# merchant_bot.polling(none_stop=True, interval=0)
