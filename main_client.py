import django
import os

from django.shortcuts import get_object_or_404
from telegram import InputFile

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()
# from email import message
# from re import T
import telebot
from telebot import types
from requests import get
import time
from product.models import TelegramUser, Product, Basket
import urllib.request

bot = telebot.TeleBot('5388600014:AAHFGhuoNaXEK7dcd-qRi0okx-Wa2S5Gs2U')
print(time.ctime())
time.sleep(3)

url_menu = 'http://localhost:8000/api/v1/menu/'
url_category = 'http://localhost:8000/api/v1/category/'

response_menu = get(url_menu).json()
response_categories = get(url_category).json()


# def response_category():
#     for response in response_categories:
#         return response


def response_menus():
    for response in response_menu:
        return response


# user_id = [965045581, 717825368]
# user_phone = []


def telegram_user_id():
    user = []
    for user_id in TelegramUser.objects.all():
        user.append(user_id)
    return user


def checking_for_an_empty_field():
    if telegram_user_id() is None:
        return 'xxxx'
    else:
        return telegram_user_id()


def product():
    for product in Product.objects.all():
        return product


@bot.message_handler(commands=["start"])
def start(m):
    # print(m.from_user.id)
    print(type(m.from_user.id))
    print(type(checking_for_an_empty_field()))
    # print(checking_for_an_empty_field())

    if TelegramUser.objects.filter(user_id=m.from_user.id):
        # print(m.from_user.first_name, m.from_user.last_name)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg = bot.send_message(m.chat.id, f'Приветствую Вас {m.from_user.first_name}!', reply_markup=keyboard)
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in ['Меню', 'Корзина']])
        # keyboard.add(
        #     *[types.KeyboardButton(bot_message) for bot_message in ['Выполненные заказы', 'Перейти в админ-панель']])
        bot.send_message(m.chat.id, 'Выберите в меню операции!', reply_markup=keyboard)
        bot.register_next_step_handler(msg, bot_message)
    else:  # (m.from_user.id) == (users.user_id):
        # print(m.from_user)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text='Поделиться номером', request_contact=True))
        bot.send_message(m.chat.id, 'Поделиться номером!', reply_markup=keyboard)


@bot.message_handler(content_types=["text", "contact"])
def bot_message(m):
    # print(m.text)
    # print(m)
    if m.contact is not None:
        # print(1)
        # print(m.contact)
        TelegramUser.objects.get_or_create(user_id=m.contact.user_id, first_name=m.contact.first_name,
                                           last_name=m.contact.last_name, phone_number=m.contact.phone_number,
                                           vcard=m.contact.vcard)
        # print(m.contact)
        bot.send_message(m.chat.id, f'Пользователь добавлен в базу {m.contact}')
        start(m)

    elif m.text == 'Меню':
        # print(m)
        for response_category in response_categories:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            category = types.InlineKeyboardButton(text=f"123{response_category['category_name']}",
                                                  callback_data=f"{response_category['category_name']}")

            keyboard.add(category)
            bot.send_message(m.chat.id, f"{response_category['category_name']}", reply_markup=keyboard)

    elif m.text == 'Заказы в процессе':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton('Список Заказов в процессе'))
        keyboard.add(types.KeyboardButton('В начало'))
        bot.send_message(m.chat.id, 'Нажмите на Список Заказов в процессе', reply_markup=keyboard)

    elif m.text == 'Список Заказов в процессе':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        orders_in_progress_1 = types.InlineKeyboardButton(text='Заказ в процессе №1',
                                                          callback_data='orders_in_progress_1')
        orders_in_progress_2 = types.InlineKeyboardButton(text="Заказ в процессе №2",
                                                          callback_data="orders_in_progress_2")
        orders_in_progress_3 = types.InlineKeyboardButton(text="Заказ в процессе №3",
                                                          callback_data="orders_in_progress_3")
        orders_in_progress_4 = types.InlineKeyboardButton(text="Заказ в процессе №4",
                                                          callback_data="orders_in_progress_4")
        orders_in_progress_5 = types.InlineKeyboardButton(text="Заказ в процессе №5",
                                                          callback_data="orders_in_progress_5")
        orders_in_progress_6 = types.InlineKeyboardButton(text="Заказ в процессе №6",
                                                          callback_data="orders_in_progress_6")
        orders_in_progress_7 = types.InlineKeyboardButton(text="Заказ в процессе №7",
                                                          callback_data="orders_in_progress_7")
        orders_in_progress_8 = types.InlineKeyboardButton(text="Заказ в процессе №8",
                                                          callback_data="orders_in_progress_8")
        keyboard.add(orders_in_progress_1, orders_in_progress_2, orders_in_progress_3, orders_in_progress_4,
                     orders_in_progress_5, orders_in_progress_6, orders_in_progress_7, orders_in_progress_8)
        bot.send_message(m.chat.id, "Список Заказов в процессе", reply_markup=keyboard)

    elif m.text == 'Выполненные заказы':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton('Список Выполненных заказов'))
        keyboard.add(types.KeyboardButton('В начало'))
        bot.send_message(m.chat.id, 'Нажмите на Список Выполненных заказов', reply_markup=keyboard)
        # bot.send_photo(m.chat.id, 'https://cs13.pikabu.ru/images/big_size_comm/2020-06_3/159194100716237333.jpg')

    elif m.text == 'Список Выполненных заказов':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        completed_orders_1 = types.InlineKeyboardButton(text='Заказ №1', callback_data='completed_orders_1')
        completed_orders_2 = types.InlineKeyboardButton(text="Заказ №2", callback_data="completed_orders_2")
        completed_orders_3 = types.InlineKeyboardButton(text="Заказ №3", callback_data="completed_orders_3")
        completed_orders_4 = types.InlineKeyboardButton(text="Заказ №4", callback_data="completed_orders_4")
        completed_orders_5 = types.InlineKeyboardButton(text="Заказ №5", callback_data="completed_orders_5")
        completed_orders_6 = types.InlineKeyboardButton(text="Заказ №6", callback_data="completed_orders_6")
        completed_orders_7 = types.InlineKeyboardButton(text="Заказ №7", callback_data="completed_orders_7")
        completed_orders_8 = types.InlineKeyboardButton(text="Заказ №8", callback_data="completed_orders_8")
        keyboard.add(completed_orders_1, completed_orders_2, completed_orders_3, completed_orders_4, completed_orders_5,
                     completed_orders_6, completed_orders_7, completed_orders_8)
        bot.send_message(m.chat.id, "Список Выполненных заказов", reply_markup=keyboard)


    elif m.text == 'Перейти в админ-панель':
        bot.send_message(m.chat.id, '[Перейти в админ-панель](http://www.google.com/)', parse_mode='Markdown')
        # keyboard = types.InlineKeyboardMarkup(row_width=1)
        # keyboard.add(types.InlineKeyboardButton(text='Перейти в админ-панель',url='https://www.google.kz/'))
        # bot.send_photo(m.chat.id, 'Перейти в админ-панель', reply_markup=keyboard)

    elif m.text == 'В начало':
        print(m.from_user.first_name, m.from_user.last_name)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg = bot.send_message(m.chat.id, 'В начало', reply_markup=keyboard)
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in ['Новые заказы', 'Заказы в процессе']])
        keyboard.add(
            *[types.KeyboardButton(bot_message) for bot_message in ['Выполненные заказы', 'Перейти в админ-панель']])
        bot.send_message(m.chat.id, 'В начало, Выберите в меню операции!', reply_markup=keyboard)
        bot.register_next_step_handler(msg, bot_message)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    for menu in response_menu:

        if call.data == menu['category']:
            for response_category in response_categories:
                if menu['category'] == response_category['category_name']:
                    # print(call)
                    # print(call.data)
                    keyboard = types.InlineKeyboardMarkup(row_width=2)

                    print(menu['photo'][1:])

                    photo = open(menu['photo'][1:], 'rb')
                    bot.send_photo(call.message.chat.id, photo)

                    add_menu = types.InlineKeyboardButton(text=f"++ в корзину-{menu['id']}",
                                                          callback_data=f"add_menu_{menu['id']}")
                    subtract_menu = types.InlineKeyboardButton(text=f"-- с корзины-{menu['id']}",
                                                               callback_data=f"subtract_menu_{menu['id']}")
                    keyboard.add(add_menu, subtract_menu)

                    bot.send_message(call.message.chat.id, f"{menu}", reply_markup=keyboard)

                    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    # markup.add(types.KeyboardButton('Назад меню категории'))
                    # markup.add(types.KeyboardButton('Корзина'))
                    # bot.send_message(call.message.chat.id, menu['id'], reply_markup=markup)

        elif call.data == f"add_menu_{menu['id']}":
            if not Basket.objects.filter(product_id=menu['id'], telegram_user_id=call.from_user.id):
                Basket.objects.create(
                    amount=1,
                    product_id=menu['id'],
                    telegram_user_id=call.from_user.id,
                    product_total_price=menu['price'],
                )
            elif Basket.objects.filter(product_id=menu['id'], telegram_user_id=call.from_user.id):
                basket = get_object_or_404(Basket, product_id=menu['id'])
                basket.amount += 1
                basket.product_total_price += menu['price']
                basket.save()

        elif call.data == f"subtract_menu_{menu['id']}":
            if Basket.objects.filter(amount__gt=1, product_id=menu['id'], telegram_user_id=call.from_user.id):
                basket = get_object_or_404(Basket, product_id=menu['id'])
                basket.amount -= 1
                basket.product_total_price -= menu['price']
                basket.save()
            elif Basket.objects.filter(amount=1, product_id=menu['id'], telegram_user_id=call.from_user.id):
                basket = Basket.objects.filter(amount=1, product_id=menu['id'], telegram_user_id=call.from_user.id)
                basket.delete()




        elif call.data == "new_order_1" or call.data == "new_order_2" or call.data == "new_order_3" or call.data == "new_order_4" or call.data == "new_order_5" or call.data == "new_order_6" or call.data == "new_order_7" or call.data == "new_order_8":
            # print(call)
            # print(call.data)
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            call_the_client = types.InlineKeyboardButton(text="Созвониться с клиентом",
                                                         callback_data="call_the_client")
            accept_order = types.InlineKeyboardButton(text="Принять заказ", callback_data="accept_order")
            keyboard.add(call_the_client, accept_order)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Клиент: {call.from_user.first_name, call.from_user.last_name} \n Номер Заказа: 3 \n Блюда: \n  Гамбургер говяжий двойной \n 1шт. х 1200т. = 1200 тг. \n Соус горчичный: \n 2шт. х 100 тг. = 100 тг.",
                                  reply_markup=keyboard)
        elif call.data == "call_the_client":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Клиент: {call.from_user.first_name, call.from_user.last_name} \n Телефон номер: user_phone",
                                  reply_markup=keyboard)
        elif call.data == "accept_order":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Клиенту: {call.from_user.first_name, call.from_user.last_name} отправлено уведомление",
                                  reply_markup=keyboard)

        elif call.data == 'orders_in_progress_1' or call.data == 'orders_in_progress_2' or call.data == 'orders_in_progress_3' or call.data == 'orders_in_progress_4' or call.data == 'orders_in_progress_5' or call.data == 'orders_in_progress_6' or call.data == 'orders_in_progress_7' or call.data == 'orders_in_progress_8':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Клиент: {call.from_user.first_name, call.from_user.last_name} \n Номер Заказа: 3 \n Блюда: \n  Гамбургер говяжий двойной \n 1шт. х 1200т. = 1200 тг. \n Соус горчичный: \n 2шт. х 100 тг. = 100 тг. \n\n\n Заказ завершен")

        elif call.data == "completed_orders_1" or call.data == "completed_orders_2" or call.data == "completed_orders_3" or call.data == "completed_orders_4" or call.data == "completed_orders_5" or call.data == "completed_orders_6" or call.data == "completed_orders_7" or call.data == "completed_orders_8":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            customer_feedback = types.InlineKeyboardButton(text="Отзыв клиента", callback_data="customer_feedback")
            keyboard.add(customer_feedback)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Клиент: {call.from_user.first_name, call.from_user.last_name} \n Номер Заказа: 3 \n Блюда: \n  Гамбургер говяжий двойной \n 1шт. х 1200т. = 1200 тг. \n Соус горчичный: \n 2шт. х 100 тг. = 100 тг.",
                                  reply_markup=keyboard)

        elif call.data == "customer_feedback":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Блюда: \n\n  Гамбургер говяжий двойной \n 1шт. х 1200т. = 1200 тг. \n\n Соус горчичный: \n\n 2шт. х 100 тг. = 100 тг. \n\n\n Отзыв: \n Очень вкусно, но слишком долго выполняется заказ")


bot.polling(none_stop=True, interval=0)
