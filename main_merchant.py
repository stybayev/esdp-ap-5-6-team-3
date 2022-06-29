import os
from urllib import request

from config import merchant_key

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django
django.setup()
from accounts.views import register

import telebot
from telebot import types
import time
from product.models import (TelegramUser,
                            MerchantTelegramUser,
                            ShoppingCartOrder)


merchant_bot = telebot.TeleBot(merchant_key)

print(time.ctime())
time.sleep(3)


@merchant_bot.message_handler(commands=["start"])
def start(m):
    print(type(m.from_user.id))

    if MerchantTelegramUser.objects.filter(user_id=m.from_user.id):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in ['Новые заказы']])
        # keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in ['Новые заказы', 'Заказы в процессе']])
        # keyboard.add(
        #     *[types.KeyboardButton(bot_message) for bot_message in ['Выполненные заказы', 'Перейти в админ-панель']])

        merchant_bot.send_message(m.chat.id, f'Приветствую Вас *{m.from_user.first_name}*!',
                                  reply_markup=keyboard, parse_mode="Markdown")
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text='\U0001F4F2Поделиться номером', request_contact=True))
        merchant_bot.send_message(m.chat.id, '\U0001F4F2Поделиться номером!', reply_markup=keyboard)


@merchant_bot.message_handler(content_types=["text", "contact"])
def bot_message(m):
    if m.contact is not None:
        register(request, m)
        merchant_bot.send_message(m.chat.id, f'Пользователь *{m.contact.first_name} {m.contact.last_name} '
                                             f'{m.contact.phone_number}* добавлен в базу \U0001F4BB',
                                  parse_mode="Markdown")
        merchant_bot.send_message(m.chat.id, f'Вы автоматическии зарегистрированы в Админ панеле \n'
                                             f'на вход систему используйте нижеуказанные Лигин и пароль \n'
                                             f'Логин: *{m.contact.user_id}*  Пароль *{m.contact.phone_number}*',
                                  parse_mode="Markdown")
        start(m)

    elif m.text == 'Новые заказы':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton('Список Новых заказов'))
        keyboard.add(types.KeyboardButton('В начало'))
        merchant_bot.send_message(m.chat.id, 'Нажмите на Список новых заказов', reply_markup=keyboard)

    elif m.text == 'Список Новых заказов':
        for shop_cart in ShoppingCartOrder.objects.filter(status=1):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            new_order = types.InlineKeyboardButton(text=f'Заказ №{shop_cart.id}', url=f"http://127.0.0.1:8000/order/{shop_cart.id}")
            keyboard.add(new_order)
            merchant_bot.send_message(m.chat.id, f"Заказ *№{shop_cart.id}* "
                                                 f"*{shop_cart.telegram_user_id.first_name}* "
                                                 f"*{shop_cart.sum_product_total_price()}*+"
                                                 f"*{shop_cart.service_price()}%* = "
                                                 f"итого *{shop_cart.total_sum()}* тенге"

                                                 ,
                                      reply_markup=keyboard, parse_mode="Markdown")

    elif m.text == 'В начало':
        print(m.from_user.first_name, m.from_user.last_name)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in ['Новые заказы', ]])
        merchant_bot.send_message(m.chat.id, 'В начало, Выберите в меню операции!', reply_markup=keyboard)


@merchant_bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "new_order_1" or call.data == "new_order_2" or call.data == "new_order_3" or call.data == "new_order_4" or call.data == "new_order_5" or call.data == "new_order_6" or call.data == "new_order_7" or call.data == "new_order_8":
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        call_the_client = types.InlineKeyboardButton(text="Созвониться с клиентом", callback_data="call_the_client")
        accept_order = types.InlineKeyboardButton(text="Принять заказ", callback_data="accept_order")
        keyboard.add(call_the_client, accept_order)
        merchant_bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       text=f"Клиент: {call.from_user.first_name, call.from_user.last_name} \n Номер Заказа: 3 \n Блюда: \n  Гамбургер говяжий двойной \n 1шт. х 1200т. = 1200 тг. \n Соус горчичный: \n 2шт. х 100 тг. = 100 тг.",
                                       reply_markup=keyboard)
    elif call.data == "call_the_client":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        merchant_bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       text=f"Клиент: {call.from_user.first_name, call.from_user.last_name} \n Телефон номер: {user_phone[0]}",
                                       reply_markup=keyboard)
    elif call.data == "accept_order":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        merchant_bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       text=f"Клиенту: {call.from_user.first_name, call.from_user.last_name} отправлено уведомление",
                                       reply_markup=keyboard)

    elif call.data == 'orders_in_progress_1' or call.data == 'orders_in_progress_2' or call.data == 'orders_in_progress_3' or call.data == 'orders_in_progress_4' or call.data == 'orders_in_progress_5' or call.data == 'orders_in_progress_6' or call.data == 'orders_in_progress_7' or call.data == 'orders_in_progress_8':
        merchant_bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       text=f"Клиент: {call.from_user.first_name, call.from_user.last_name} \n Номер Заказа: 3 \n Блюда: \n  Гамбургер говяжий двойной \n 1шт. х 1200т. = 1200 тг. \n Соус горчичный: \n 2шт. х 100 тг. = 100 тг. \n\n\n Заказ завершен")

    elif call.data == "completed_orders_1" or call.data == "completed_orders_2" or call.data == "completed_orders_3" or call.data == "completed_orders_4" or call.data == "completed_orders_5" or call.data == "completed_orders_6" or call.data == "completed_orders_7" or call.data == "completed_orders_8":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        customer_feedback = types.InlineKeyboardButton(text="Отзыв клиента", callback_data="customer_feedback")
        keyboard.add(customer_feedback)
        merchant_bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       text=f"Клиент: {call.from_user.first_name, call.from_user.last_name} \n Номер Заказа: 3 \n Блюда: \n  Гамбургер говяжий двойной \n 1шт. х 1200т. = 1200 тг. \n Соус горчичный: \n 2шт. х 100 тг. = 100 тг.",
                                       reply_markup=keyboard)

    elif call.data == "customer_feedback":
        merchant_bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       text=f"Блюда: \n\n  Гамбургер говяжий двойной \n 1шт. х 1200т. = 1200 тг. \n\n Соус горчичный: \n\n 2шт. х 100 тг. = 100 тг. \n\n\n Отзыв: \n Очень вкусно, но слишком долго выполняется заказ")


merchant_bot.polling(none_stop=True, interval=0)
