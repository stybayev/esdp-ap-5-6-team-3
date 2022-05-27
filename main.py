import django
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()
# from email import message
# from re import T
import telebot
from telebot import types
from requests import get
import time
from product.models import TelegramUser

bot = telebot.TeleBot('5388600014:AAHFGhuoNaXEK7dcd-qRi0okx-Wa2S5Gs2U')
print(time.ctime())
time.sleep(3)


user_id = [965045581, 717825368]
# user_phone = []


def telegram_user_id():
    for user_id in TelegramUser.objects.all():
        return user_id


def checking_for_an_empty_field():
    if telegram_user_id() is None:
        return 'xxxx'
    else:
        return telegram_user_id().user_id


@bot.message_handler(commands=["start"])
def start(m):
    # print(m.from_user.id)
    print(type(m.from_user.id))
    print(type(checking_for_an_empty_field()))
    if str(m.from_user.id) not in str(checking_for_an_empty_field()):
        # print(m.from_user)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text='Поделиться номером', request_contact=True))
        bot.send_message(m.chat.id, 'Выберите в меню операции!', reply_markup=keyboard)

    else:
        # print(m.from_user.first_name, m.from_user.last_name)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg = bot.send_message(m.chat.id, f'Приветствую Вас {m.from_user.first_name}!', reply_markup=keyboard)

        # keyboard.add(types.KeyboardButton(text='Поделиться номером', request_contact=True))

        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in ['Новые заказы', 'Заказы в процессе']])
        keyboard.add(
            *[types.KeyboardButton(bot_message) for bot_message in ['Выполненные заказы', 'Перейти в админ-панель']])
        bot.send_message(m.chat.id, 'Выберите в меню операции!', reply_markup=keyboard)
        bot.register_next_step_handler(msg, bot_message)

# @bot.message_handler(commands=["start"])
# def start(m):
#     # print(m.from_user.id)
#
#     # if str(m.from_user.id) not in telegram_user_id().user_id:
#     print((checking_for_an_empty_field()))
#     if str(m.from_user.id) not in checking_for_an_empty_field():
#
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         msg = bot.send_message(m.chat.id, f'Приветствую Вас {m.from_user.first_name}!', reply_markup=keyboard)
#
#         keyboard.add(types.KeyboardButton(text='Поделиться номером', request_contact=True))
#         bot.send_message(m.chat.id, 'Выберите в меню операции!', reply_markup=keyboard)
#         # print(m.contact)
#         # print(user_id)
#         # bot.register_next_step_handler(msg, bot_message)
#     else:
#         # print(m.from_user.first_name, m.from_user.last_name)
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         msg = bot.send_message(m.chat.id, f'Приветствую Вас {m.from_user.first_name}!', reply_markup=keyboard)
#
#         # keyboard.add(types.KeyboardButton(text='Поделиться номером', request_contact=True))
#
#         keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in ['Новые заказы', 'Заказы в процессе']])
#         keyboard.add(
#             *[types.KeyboardButton(bot_message) for bot_message in ['Выполненные заказы', 'Перейти в админ-панель']])
#         # bot.send_message(m.chat.id, 'Выберите в меню операции!', reply_markup=keyboard)
#         bot.register_next_step_handler(msg, bot_message)
# @bot.message_handler(commands=["start"])
# def start(m):
#     print(m.from_user.id)
#
#     if m.from_user.id not in user_id:
#         print(m.from_user.first_name, m.from_user.last_name)
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         msg = bot.send_message(m.chat.id, f'Приветствую Вас {m.from_user.first_name}!', reply_markup=keyboard)
#
#         keyboard.add(types.KeyboardButton(text='Поделиться номером', request_contact=True))
#
#         # keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in ['Новые заказы', 'Заказы в процессе']])
#         # keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in ['Выполненные заказы', 'Перейти в админ-панель']])
#         bot.send_message(m.chat.id, 'Выберите в меню операции!', reply_markup=keyboard)
#         # print(m.contact)
#         # print(user_id)
#         # bot.register_next_step_handler(msg, bot_message)
#     else:
#         print(m.from_user.first_name, m.from_user.last_name)
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         msg = bot.send_message(m.chat.id, f'Приветствую Вас {m.from_user.first_name}!', reply_markup=keyboard)
#
#         # keyboard.add(types.KeyboardButton(text='Поделиться номером', request_contact=True))
#
#         keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in ['Новые заказы', 'Заказы в процессе']])
#         keyboard.add(
#             *[types.KeyboardButton(bot_message) for bot_message in ['Выполненные заказы', 'Перейти в админ-панель']])
#         bot.send_message(m.chat.id, 'Выберите в меню операции!', reply_markup=keyboard)
#         bot.register_next_step_handler(msg, bot_message)


# @bot.message_handler(commands=["nummer"])
# def phone(m):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(types.KeyboardButton(text='Поделиться номером', request_contact=True))
#     bot.send_message(m.chat.id, 'Phone number', reply_markup=keyboard)

# @bot.message_handler(content_types=["contact"])
# def contact(m):
#     if m.contact is not None:
#         print(m.contact)
#         bot.send_message(m.chat.id, f'{m.contact}')

@bot.message_handler(content_types=["text", "contact"])
def bot_message(m):
    # print(m.text)
    # print(m)
    if m.contact is not None:
        print(1)
        print(m.contact)
        TelegramUser.objects.get_or_create(user_id=m.contact.user_id, first_name=m.contact.first_name,
                                           last_name=m.contact.last_name, phone_number=m.contact.phone_number,
                                           vcard=m.contact.vcard)
        print(m.contact)
        # print(m)
        # user_id.append(m.contact.user_id)
        # user_phone.append(m.contact.phone_number)
        # print(user_id)
        bot.send_message(m.chat.id, f'Позже уберем {m.contact}')
        start(m)


    elif m.text == 'Новые заказы':
        # TelegramUser.objects.update_or_create(user_id=m.contact.user_id, first_name=m.contact.first_name,
        #                                       last_name=m.contact.last_name, phone_number=m.contact.phone_number,
        #                                       vcard=m.contact.vcard)

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton('Список Новых заказов'))
        keyboard.add(types.KeyboardButton('В начало'))
        bot.send_message(m.chat.id, 'Нажмите на Список новых заказов', reply_markup=keyboard)

        # keyboardmain = types.InlineKeyboardMarkup(row_width=1)
        # order_1 = types.InlineKeyboardButton(text="Заказ №1", callback_data="order_1")
        # order_2 = types.InlineKeyboardButton(text="Заказ №2", callback_data="order_2")
        # order_3 = types.InlineKeyboardButton(text="Заказ №3", callback_data="order_3")
        # order_4 = types.InlineKeyboardButton(text="Заказ №4", callback_data="order_4")
        # order_5 = types.InlineKeyboardButton(text="Заказ №5", callback_data="order_5")
        # order_6 = types.InlineKeyboardButton(text="Заказ №6", callback_data="order_6")
        # order_7 = types.InlineKeyboardButton(text="Заказ №7", callback_data="order_7")
        # order_8 = types.InlineKeyboardButton(text="Заказ №8", callback_data="order_8")
        # keyboardmain.add(order_1, order_2, order_3, order_4, order_5, order_6, order_7, order_8)
        # bot.send_message(m.chat.id, "Список новых заказов", reply_markup=keyboardmain)

    elif m.text == 'Список Новых заказов':
        # print(m)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        new_order_1 = types.InlineKeyboardButton(text='Заказ №1', callback_data='new_order_1')
        # print(order_1)
        new_order_2 = types.InlineKeyboardButton(text="Заказ №2", callback_data="new_order_2")
        new_order_3 = types.InlineKeyboardButton(text="Заказ №3", callback_data="new_order_3")
        new_order_4 = types.InlineKeyboardButton(text="Заказ №4", callback_data="new_order_4")
        new_order_5 = types.InlineKeyboardButton(text="Заказ №5", callback_data="new_order_5")
        new_order_6 = types.InlineKeyboardButton(text="Заказ №6", callback_data="new_order_6")
        new_order_7 = types.InlineKeyboardButton(text="Заказ №7", callback_data="new_order_7")
        new_order_8 = types.InlineKeyboardButton(text="Заказ №8", callback_data="new_order_8")
        keyboard.add(new_order_1, new_order_2, new_order_3, new_order_4, new_order_5, new_order_6, new_order_7,
                     new_order_8)
        bot.send_message(m.chat.id, "Список новых заказов", reply_markup=keyboard)

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
    if call.data == "new_order_1" or call.data == "new_order_2" or call.data == "new_order_3" or call.data == "new_order_4" or call.data == "new_order_5" or call.data == "new_order_6" or call.data == "new_order_7" or call.data == "new_order_8":
        # print(call)
        # print(call.data)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        call_the_client = types.InlineKeyboardButton(text="Созвониться с клиентом", callback_data="call_the_client")
        accept_order = types.InlineKeyboardButton(text="Принять заказ", callback_data="accept_order")
        keyboard.add(call_the_client, accept_order)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Клиент: {call.from_user.first_name, call.from_user.last_name} \n Номер Заказа: 3 \n Блюда: \n  Гамбургер говяжий двойной \n 1шт. х 1200т. = 1200 тг. \n Соус горчичный: \n 2шт. х 100 тг. = 100 тг.",
                              reply_markup=keyboard)
    elif call.data == "call_the_client":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Клиент: {call.from_user.first_name, call.from_user.last_name} \n Телефон номер: {user_phone[0]}",
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

# @bot.message_handler(commands=["start"])
# def start(m):
#     print(m.from_user.first_name, m.from_user.last_name)
#     keyboard = types.ReplyKeyboardMarkup(row_width=3)
#     msg = bot.send_message(m.chat.id, f'Приветствую Вас {m.from_user.first_name}!', reply_markup=keyboard)
#     keyboard.add(*[types.KeyboardButton(name) for name in ['Новые заказы', 'Заказы в процессе']])
#     # keyboard.add(*[types.KeyboardButton(name) for name in ['Выполненные заказы']])

#     keyboard.add(types.KeyboardButton('Начало'))
#     bot.send_message(m.chat.id, 'Выберите в меню операции!',
#         reply_markup=keyboard)
#     bot.register_next_step_handler(msg, name)

# def name(m):
#     print(m.text)
#     print(m)
#     if m.text == 'Новые заказы':
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         keyboard.add(*[types.KeyboardButton(advert) for advert in ['Подробнее о заказе']])
#         keyboard.add(*[types.KeyboardButton(advert) for advert in ['В начало']])
#         bot.send_message(m.chat.id, 'нажмите на подробнее',
#             reply_markup=keyboard)
#     elif m.text == 'Подробнее о заказе':
#         bot.send_message(m.chat.id, 'id заказа', reply_markup=keyboard)
#         bot.send_message(m.chat.id, 'id пользователя', reply_markup=keyboard)
#     elif m.text == 'Заказы в процессе':
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         keyboard.add(*[types.KeyboardButton(advert) for advert in ['Подробнее о заказе']])
#         keyboard.add(*[types.KeyboardButton(advert) for advert in ['В начало']])
#         bot.send_message(m.chat.id, 'id заказа',
#             reply_markup=keyboard)
#     elif m.text == 'Выполненные заказы':
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         keyboard.add(*[types.KeyboardButton(advert) for advert in ['В начало']])
#         keyboard.add(*[types.KeyboardButton(advert) for advert in ['Подробнее о заказе']])
#         bot.send_message(m.chat.id, 'id заказа', reply_markup=keyboard)
#         bot.send_photo(m.chat.id,
#                        'https://cs13.pikabu.ru/images/big_size_comm/2020-06_3/159194100716237333.jpg')
#     elif m.text == 'В начало':
#         print(1)
#         bot.send_message(m.chat.id, "Вы вернулись в меню", reply_markup=keyboard.start())


# bot.polling(none_stop=True, interval=0)


# --------------------------------------------------------

# @bot.message_handler(commands=["start"])
# def any_msg(message):
# keyboardmain = types.InlineKeyboardMarkup(row_width=2)
# first_button = types.InlineKeyboardButton(text="1button", callback_data="first")
# second_button = types.InlineKeyboardButton(text="2button", callback_data="second")
# second = types.InlineKeyboardButton(text="3button", callback_data="second2")
# sec = types.InlineKeyboardButton(text="4button", callback_data="second3")
# keyboardmain.add(first_button, second_button, second, sec)
# bot.send_message(message.chat.id, "testing kb", reply_markup=keyboardmain)

# @bot.callback_query_handler(func=lambda call:True)
# def callback_inline(call):
#     if call.data == "mainmenu":

#         keyboardmain = types.InlineKeyboardMarkup(row_width=2)
# first_button = types.InlineKeyboardButton(text="1button", callback_data="first")
# second_button = types.InlineKeyboardButton(text="2button", callback_data="second")
# keyboardmain.add(first_button, second_button)
#         bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="menu",reply_markup=keyboardmain)

#     if call.data == "first":
#         keyboard = types.InlineKeyboardMarkup()
#         rele1 = types.InlineKeyboardButton(text="1t", callback_data="1")
#         rele2 = types.InlineKeyboardButton(text="2t", callback_data="2")
#         rele3 = types.InlineKeyboardButton(text="3t", callback_data="3")
#         backbutton = types.InlineKeyboardButton(text="back123", callback_data="mainmenu")
#         keyboard.add(rele1, rele2, rele3, backbutton)
#         bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="replaced text",reply_markup=keyboard)

#     elif call.data == "second":
#         keyboard = types.InlineKeyboardMarkup()
#         rele1 = types.InlineKeyboardButton(text="another layer", callback_data="gg")
#         backbutton = types.InlineKeyboardButton(text="back", callback_data="mainmenu")
#         keyboard.add(rele1,backbutton)
#         bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="replaced text",reply_markup=keyboard)

#     elif call.data == "1" or call.data == "2" or call.data == "3":
#         bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="alert")
#         keyboard3 = types.InlineKeyboardMarkup()
#         button = types.InlineKeyboardButton(text="lastlayer", callback_data="ll")
#         keyboard3.add(button)
#         bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="last layer",reply_markup=keyboard3)


# if __name__ == "__main__":
#     bot.polling(none_stop=True)
# --------------------------------------------------------
