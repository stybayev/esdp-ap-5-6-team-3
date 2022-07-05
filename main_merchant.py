import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django
django.setup()
from urllib import request
from accounts.views import register, change_password
import telebot
from telebot import types
import time
from product.models import (MerchantTelegramUser,
                            ShoppingCartOrder)
from config import merchant_key


merchant_bot = telebot.TeleBot(merchant_key)
url_crm = 'http://127.0.0.1:8000'
print(time.ctime())
time.sleep(3)


@merchant_bot.message_handler(commands=["start"])
def start(m):
    """
        Функция для начального запуска маркап кнопок,
        проверяет мерчанта на регистрацию
    """
    print(type(m.from_user.id))
    if MerchantTelegramUser.objects.filter(user_id=m.from_user.id):
        """
            Если мерчант ранее зарегистрирован в базе, то отправляет
            приветственную текст мерчанту и вызывает маркап кнопки:
        """
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(bot_message) for
                       bot_message in ['Новые заказы', 'Сброс пароля']])
        merchant_bot.send_message(
            m.chat.id, f'Приветствую Вас *{m.from_user.first_name}*!',
            reply_markup=keyboard, parse_mode="Markdown")
    else:
        """
            Если мерчант не зарегистрирован в базе, то выводит
            маркап кнопку 'Поделиться номером'
        """
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(
            text='\U0001F4F2Поделиться номером', request_contact=True))
        merchant_bot.send_message(
            m.chat.id, '\U0001F4F2Поделиться номером!',
            reply_markup=keyboard)


@merchant_bot.message_handler(content_types=["text", "contact"])
def bot_message(m):
    if m.contact is not None:
        """
            Если мерчант не зарегистрирован в Базе, то посленажатие
            на кнопку 'Поделиться номером!' данные мерчанта (Имя,
            Фамилия, Телефон, Телеграмм ID) сохраняется в БД модели
            MerchantTelegramUser, также производиться регистрация
            пользователя в Админ панеле, т.е. создается аутентификационный
            логин и пароль
        """
        register(request, m)
        merchant_bot.send_message(
            m.chat.id, f'Пользователь *{m.contact.first_name} '
                       f'{m.contact.last_name} '
            f'{m.contact.phone_number}* добавлен в базу \U0001F4BB',
            parse_mode="Markdown")
        merchant_bot.send_message(
            m.chat.id, f'Вы автоматическии зарегистрированы в Админ панеле \n'
            f'на вход систему используйте нижеуказанные Лигин и пароль \n'
            f'Логин: *{m.contact.user_id}*  Пароль *{m.contact.phone_number}*',
            parse_mode="Markdown")
        start(m)

    elif m.text == 'Сброс пароля':
        """
            Производиться сброс пароля на Админ панель
        """
        change_password(request, m)
        for merchant in MerchantTelegramUser.objects.all():
            if merchant.user_id == m.chat.id:
                merchant_bot.send_message(
                    m.chat.id,
                    f'_Пароль сброшен на_ *{merchant.phone_number[1:]}*',
                    parse_mode="Markdown")

    elif m.text == 'Новые заказы':
        """
            После нажатие на маркап кнопку "Новые заказы" выводиться две новых
            маркап кнопок 'Список Новых заказов' и 'В начало'
        """
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton('Список Новых заказов'))
        keyboard.add(types.KeyboardButton('В начало'))
        merchant_bot.send_message(
            m.chat.id, 'Нажмите на Список новых заказов',
            reply_markup=keyboard)

    elif m.text == 'Список Новых заказов':
        """
            После нажатие на маркап кнопку 'Список Новых заказов'
            выводиться инлайн URL кнопки новых заказо, при нажатие
            на эти URL кнопки происходит переход на Админ панель
            в страницу заказа
        """
        for shop_cart in ShoppingCartOrder.objects.filter(status=1):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            new_order = types.InlineKeyboardButton(
                text=f'Заказ №{shop_cart.id}',
                url=f"{url_crm}/order/{shop_cart.id}")
            keyboard.add(new_order)
            merchant_bot.send_message(
                m.chat.id, f"Заказ *№{shop_cart.id}* "
                f"*{shop_cart.telegram_user_id.first_name}*"
                f"*{shop_cart.sum_product_total_price()}*+"
                f"*{shop_cart.service_price()}%* = "
                f"итого *{shop_cart.total_sum()}* тенге",
                reply_markup=keyboard, parse_mode="Markdown")

    elif m.text == 'В начало':
        """
            При нажатие на маркап кнопку 'В начало' возвращется в главный меню
            где отображается маркап кнопки 'Новые заказы' и 'Сброс пароля'
        """
        keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(bot_message) for
                       bot_message in ['Новые заказы', 'Сброс пароля']])
        merchant_bot.send_message(
            m.chat.id, 'В начало, Выберите в меню операции!',
            reply_markup=keyboard)


@merchant_bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """ Ничего не выполняет """
    if call.data == "new_order_1" or call.data == "new_order_2":
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        call_the_client = types.InlineKeyboardButton(
            text="Созвониться с клиентом", callback_data="call_the_client")
        accept_order = types.InlineKeyboardButton(
            text="Принять заказ", callback_data="accept_order")
        keyboard.add(call_the_client, accept_order)
        merchant_bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f"Клиент: "
                 f"{call.from_user.first_name, call.from_user.last_name} "
                 f"\n Номер Заказа: 3 \n Блюда: "
                 f"\n  Гамбургер говяжий двойной ",
            reply_markup=keyboard)


merchant_bot.polling(none_stop=True, interval=0)
