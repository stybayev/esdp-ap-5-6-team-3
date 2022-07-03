import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django

django.setup()
import datetime
from django.shortcuts import get_object_or_404
from config import client_key, merchant_key
import telebot
from telebot import types
from requests import get
from cal import Calendar, CallbackData, RUSSIAN_LANGUAGE, \
    get_time, TIME, get_persons, PERSONS
from telebot.types import ReplyKeyboardRemove, CallbackQuery, \
    InlineKeyboardMarkup
import time
from product.models import TelegramUser, Basket, Aboutus, BasketToOrder, \
    ShoppingCartOrder, StatusShoppingCartOrder, MerchantTelegramUser, \
    TableReservation, CustomerFeedback
from fpdf import FPDF


logger = telebot.logger
bot = telebot.TeleBot(client_key)
calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData(
    "calendar_1", "action", "year", "month", "day")
merchant_bot = telebot.TeleBot(merchant_key)

print(time.ctime())
time.sleep(3)

# # Для виртуального окружения
url_menu = 'http://localhost:8000/api/v1/menu/'
url_category = 'http://localhost:8000/api/v1/category/'
url_crm = 'http://127.0.0.1:8000'

base_url = f"https://api.telegram.org/bot{client_key}/sendPoll"
print(base_url)

# Для docker-compose
# url_menu = 'http://localhost:8080/api/v1/menu/'
# url_category = 'http://localhost:8080/api/v1/category/'
database = {}
customer_feedback = {}

response_menu = get(url_menu).json()
response_categories = get(url_category).json()


def text_basket(basket):
    """
        Функция для текстового отображение блюд, которые добавлены в корзину
    """
    basket_text = (
        f"_Наименование_: "
        f"*{basket.product.id}-{basket.product.product_name}* \n"
        f"_Цена_: *{basket.product.price}* тенге \n"
        f"_Категория_: *{basket.product.category}* \n"
        f"_Описание_: *{basket.product.description}* \n\n"
        f"_Количество_: *{basket.amount}* \n"
        f"_Сумма_: {basket.product.price}x{basket.amount}= "
        f"*{basket.product_total_price}* тенге \n")
    return basket_text


def text_menu(menu):
    """
        Функция для текстового отображание блюд в меню
    """
    menu_text = (f"_Наименование_: *{menu['id']}-{menu['product_name']}* \n"
                 f"_Цена_: *{menu['price']}* тенге \n"
                 f"_Категория_: *{menu['category']}* \n"
                 f"_Описание_: *{menu['description']}* \n")
    return menu_text


def subtract_meals(basket, menu):
    """
        Функция для изменения количества продукта в заказе, а именно убавление количества продукта в заказе
    """
    basket.amount -= 1
    basket.product_total_price -= menu['price']
    basket.save()


def add_meals(basket, menu):
    """
        Функция для изменения количества продукта в заказе, а именно добавление количества продукта в заказе
    """
    basket.amount += 1
    basket.product_total_price += menu['price']
    basket.save()


def button_basket(keyboard, basket):
    """
        Функция для инлайн кнопок, добавление и убавление количества продукта в корзине (кнопка Корзина)
    """
    add_menu = types.InlineKeyboardButton(
        text=f"\U00002795\U0001F371Добавить в корзину",
        callback_data=f"add_basket_{basket.product.id}")
    subtract_menu = types.InlineKeyboardButton(
        text=f"\U00002796\U0001F371 удалить с корзины",
        callback_data=f"subtract_basket_{basket.product.id}")
    keyboard.add(add_menu, subtract_menu)


def button_menu(keyboard, basket):
    """
        Функция для инлайн кнопок, добавление и убавление количества продукта в меню (кнопка Меню)
    """
    add_menu = types.InlineKeyboardButton(
        text=f"\U00002795\U0001F371Добавить в корзину",
        callback_data=f"add_menu_{basket.product.id}")
    subtract_menu = types.InlineKeyboardButton(
        text=f"\U00002796\U0001F371 удалить с корзины",
        callback_data=f"subtract_menu_{basket.product.id}")
    keyboard.add(add_menu, subtract_menu)


def order(call):
    """
        Функция для кнопки (Статус заказа), создает список ID заказов для
        дальнейшего сравнение с обработчиком обратного вызова (функция callback_query_handler)
    """
    value = []
    for orders in ShoppingCartOrder.objects.filter(
            telegram_user_id_id=call.from_user.id, status_id__lte=2):
        value.append(f'order_detail_{orders.id}')
    return value


@bot.message_handler(commands=["start"])
def start(m):
    """
        Функция для начального запуска маркап кнопок, проверяет клиента на регистрацию
    """
    if TelegramUser.objects.filter(user_id=m.from_user.id):
        """
            Если клиент ранее зарегистрирован в базе, то отправляет 
            приветственную текст клиенту и вызывает функцию def menu(m, text):
        """
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg = bot.send_message(
            m.chat.id, f'Приветствую Вас *{m.from_user.first_name}*!',
            reply_markup=keyboard,
            parse_mode="Markdown")
        menu(m, 'Выберите в меню операции!')
        bot.register_next_step_handler(msg, bot_message)
    else:
        """
            Если клиент не зарегистрирован в базе, то выводит 
            маркап кнопку 'Поделиться номером'
        """
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(
            text='\U0001F4F2Поделиться номером', request_contact=True))
        bot.send_message(m.chat.id, '\U0001F4F2Поделиться номером!',
                         reply_markup=keyboard)


def menu(m, text):
    """
        Функция выводит маркап кнопок для зарегистрированных клиентов
        (Меню, Корзина, О Нас, Оформить заказ, Статус заказа,
        Выполненные заказы, Забронировать столик, Оценить ресторан)
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                   ['\U0001F4D6\U0001F372\U0001F354Меню',
                    '\U0001F371Корзина']])
    keyboard.add(
        *[types.KeyboardButton(bot_message) for bot_message in
          ['\U0001F4DCО Нас', '\U0001F45DОформить заказ']])
    keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                   ['\U0001F55CСтатус заказа',
                    '\U0001F51AВыполненные заказы']])
    keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                   ['\U0001f6cb\ufe0fЗабронировать столик',
                    'Оценить ресторан']])
    bot.send_message(
        m.chat.id,
        text=text,
        reply_markup=keyboard
    )


@bot.message_handler(content_types=["text", "contact"])
def bot_message(m):
    """
        Функция для обработки маркап кнопок
    """
    if m.contact is not None:
        """
            Если клиент не зарегистрирован в Базе, то после нажатие на кнопку 'Поделиться номером!' 
            данные клиента (Имя, Фамилия, Телефон, Телеграмм ID) сохраняется в БД модели TelegramUser 
        """
        TelegramUser.objects.get_or_create(
            user_id=m.contact.user_id, first_name=m.contact.first_name,
            last_name=m.contact.last_name, phone_number=m.contact.phone_number,
            vcard=m.contact.vcard)
        bot.send_message(
            m.chat.id,
            f'Пользователь *{m.contact.first_name} {m.contact.last_name} '
            f'{m.contact.phone_number}* добавлен в базу \U0001F4BB',
            parse_mode="Markdown")
        start(m)

    elif m.text == '\U0001F4D6\U0001F372\U0001F354Меню':
        """
            После нажатие на маркап кнопку 'Меню' выводится 
            список инлайн кнопок категории продуктов
        """
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for response_category in response_categories:
            category = types.InlineKeyboardButton(
                text=f"{response_category['category_name']}-"
                     f"\U0001F355\U0001F354\U0001F379\U0001F382",
                callback_data=f"{response_category['category_name']}")

            keyboard.add(category)
        bot.send_message(
            m.chat.id,
            'Категории\U0001F4C4\U0001F355\U0001F354\U0001F379\U0001F382',
            reply_markup=keyboard, parse_mode="Markdown")

    elif m.text == '\U0001F4DCО Нас':
        """
            После нажатие на маркап кнопку 'О Нас' выводится 
            контактный номер и информация о ресторане
        """
        for about in Aboutus.objects.all():
            bot.send_message(
                m.chat.id, f"*О НАС:* \n _{about.description}_ \n\n "
                           f"Телефон: *{about.telephone_number}*",
                parse_mode="Markdown")

    elif m.text == '\U0001f6cb\ufe0fЗабронировать столик' \
            or m.text == 'Изменить бронь':
        """
            После нажатие на маркап кнопку 'Забронировать столик' выводится календарь инлайн кнопок 
        """
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
        """
        После нажатие на маркап кнопку Бронировать в базе модель TableReservation 
        создается бронь столика со статусном «Новый» и телеграмм боту мерчанта 
        отправляется уведомление о поступление бронь стола с url инлайн кнопкой. 
        После вызывается главный меню маркап кнопок (Меню, Корзина, О Нас, Оформить 
        заказ, Статус заказа, Выполненные заказы, Забронировать столик, Оценить ресторан)
        """
        TableReservation.objects.create(
            telegram_user_id_id=m.from_user.id,
            date=database[m.from_user.id]['date'],
            time=database[m.from_user.id]['time'],
            persons_number=database[m.from_user.id]['persons'])
        del database[m.from_user.id]
        for users in MerchantTelegramUser.objects.all():
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=f"Перейти в бронь столиков",
                    url=f"{url_crm}/reservations/Новый/"))

            merchant_bot.send_message(
                users.user_id,
                f'Клиент с именем {m.from_user.first_name} '
                f'назначил бронь, подтвердите',
                reply_markup=keyboard, parse_mode='Markdown')
        menu(m, "Вам придет ответа от менеджера")
    elif m.text == 'Вернуться в меню':
        """
            Маркап кнопка Вернуться в меню отменяет не завершенную операцию бронь столика
        """
        del database[m.from_user.id]
        menu(m, 'Выберите операцию')
    elif m.text == '\U0001F371Корзина':
        """
            После нажатие на маркап кнопку "Корзина", Если корзина не пуста, то выводится 
            список продуктов с фотографиями, с информацией и количество добавленных 
            продуктов на единицу продукта, после вызывается функция "def button_basket(keyboard, basket)"  
            для вызова инлайн кнопок добавление и убавление количества продукта, так же выводится 
            инлайн кнопка "Оформить заказ".
            
            Если корзина пуста, то выводится только инлайн кнопка "Меню" с уведомлением корзина пуста
        """
        order_keyboard = types.InlineKeyboardMarkup(row_width=2)

        order_processing = types.InlineKeyboardButton(
            text=f"\U0001F45D Перейти в оформление заказа",
            callback_data=f"\U0001F45DОформить заказ")
        order_keyboard.add(order_processing)
        total_sum = 0
        for basket in Basket.objects.all():
            if m.from_user.id == basket.telegram_user_id_id:
                keyboard = types.InlineKeyboardMarkup(row_width=2)

                print(f"uploads/{basket.product.photo}")

                photo = open(f"uploads/{basket.product.photo}", 'rb')

                button_basket(keyboard, basket)
                bot.send_photo(
                    m.chat.id, photo, caption=text_basket(basket),
                    reply_markup=keyboard, parse_mode="Markdown")
                total_sum += basket.product_total_price
        if Basket.objects.filter(telegram_user_id_id=m.from_user.id):
            bot.send_message(m.chat.id, f"'\n_Оформить заказ:_  \n'",
                             reply_markup=order_keyboard,
                             parse_mode='Markdown')

        if not Basket.objects.filter(telegram_user_id_id=m.from_user.id):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                types.InlineKeyboardButton(
                    text='\U0001F4D6\U0001F372\U0001F354Меню',
                    callback_data='\U0001F4D6\U0001F372\U0001F354Меню'))
            bot.send_message(
                m.chat.id,
                '<i>Корзина пуста, перейдите в</i> <ins><b>Меню</b></ins> '
                '<i>для заказа блюд</i>',
                reply_markup=keyboard, parse_mode="HTML")

    elif m.text == '\U0001F45DОформить заказ':
        """
            После нажатие на маркап кнопку 'Оформить заказ', если корзина не пуста 
            то выводится информация о продукте, количества продукта, сумма продукта, 
            итоговая сумма продукта и выводится две инлайн кнопки 'Оформить заказ' и 
            'Изменить заказ – Корзина'
            
            Если корзина пуста, то выводится инлайн кнопка 'Меню'
        """
        if not Basket.objects.filter(telegram_user_id_id=m.from_user.id):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                types.InlineKeyboardButton(
                    text='\U0001F4D6\U0001F372\U0001F354Меню',
                    callback_data='\U0001F4D6\U0001F372\U0001F354Меню'))
            bot.send_message(
                m.chat.id, f"_Заказ не можем создать, "
                           f"для начала выберите блюд из_ *Меню*  \n",
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
                    bot.send_message(
                        m.chat.id,
                        f"*{basket.product.product_name}:"
                        f"* *{basket.amount}*шт. *x* "
                        f"*{basket.product.price}*тг. = "
                        f"*{basket.product_total_price}* тенге",
                        parse_mode='Markdown')
            bot.send_message(
                m.chat.id,
                f"_Итого общая сумма продукта:_ *{total_sum}* \n"
                f"_10% за обслуживание:_ *{(total_sum * 10) / 100}* \n\n"
                f"Итого общая сумма: *{((total_sum * 10) / 100) + total_sum}*",
                reply_markup=keyboard, parse_mode='Markdown')

    elif m.text == '\U0001F55CСтатус заказа':
        """
            После нажатие на маркап кнопку 'Статус заказа' выводится активные заказы со 
            статусом еще не принято или в обработке, а также внизу заказа выводится 
            инлайн кнопка 'Детальный просмотр заказа №'
        """
        for orders in ShoppingCartOrder.objects.filter(
                telegram_user_id_id=m.from_user.id, status_id__lte=2):
            keyboard = types.InlineKeyboardMarkup(row_width=2)

            if orders.status_id == 1:
                detail_view_order = types.InlineKeyboardButton(
                    text=f"Детальный просмотр заказа №{orders.pk} \n",
                    callback_data=f'order_detail_{orders.pk}')
                keyboard.add(detail_view_order)
                bot.send_message(
                    m.chat.id, f"Заказ *№{orders.id}* еще не принято,"
                               f"\n статус: *{orders.status.status}*",
                    reply_markup=keyboard, parse_mode='Markdown')
            elif orders.status_id == 2:
                detail_view_order = types.InlineKeyboardButton(
                    text=f"Детальный просмотр заказа №{orders.pk}",
                    callback_data=f'order_detail_{orders.pk}')
                keyboard.add(detail_view_order)
                bot.send_message(
                    m.chat.id,
                    f"Заказ *№{orders.id}* принято в обработку,"
                    f"\n статус: *{orders.status.status}*",
                    reply_markup=keyboard, parse_mode='Markdown')
    elif m.text == 'Оценить ресторан':
        """
            После нажатие на маркап кнопку 'Оценить ресторан' опросник по 5 бальной шкале
        """
        bot.send_poll(
            m.chat.id, 'Оцените по 5-ти бальной шкале '
                       'степень Вашей удовлетворенности',
            is_anonymous=False, explanation="Спасибо за оценку",
            type='regular',
            options=['1 - очень плохо', '2 - плохо',
                     '3 - удовлетворительно', '4 - хорошо',
                     '5 - очень хорошо'])
    elif m.text == '\U0001F4F5Отменить оценку':
        """
            После нажатие на маркап кнопку Отменить оценку отменяет оценку очищая временную 
            оценку и вызывает главный меню маркап кнопок (Меню, Корзина, О Нас, Оформить заказ, 
            Статус заказа, Выполненные заказы, Забронировать столик, Оценить ресторан)
        """
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                       ['\U0001F4D6\U0001F372\U0001F354Меню',
                        '\U0001F371Корзина']])
        keyboard.add(
            *[types.KeyboardButton(bot_message) for bot_message in
              ['\U0001F4DCО Нас', '\U0001F45DОформить заказ']])
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                       ['\U0001F55CСтатус заказа',
                        '\U0001F51AВыполненные заказы']])
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                       ['\U0001f6cb\ufe0fЗабронировать столик',
                        'Оценить ресторан']])
        if customer_feedback == {}:
            bot.send_message(m.chat.id, 'Оценка отменен!',
                             reply_markup=keyboard)
        elif customer_feedback[m.from_user.id]:
            customer_feedback.pop(m.from_user.id)
            bot.send_message(m.chat.id, 'Оценка отменен!',
                             reply_markup=keyboard)

    elif m.text == '\U0001F51AВыполненные заказы':
        """
            После нажатие на маркап кнопку Выполненные заказы выводиться 
            список исполненных заказов в виде инлайн кнопок
        """
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for orders in ShoppingCartOrder.objects.filter(telegram_user_id_id=m.from_user.id):
            detail_view_order = types.InlineKeyboardButton(
                text=f"Заказ №{orders.pk} на сумму {orders.sum_product_total_price()} "
                     f"тенге, дата {orders.updated_at}",
                callback_data=f'completed_orders{orders.pk}')
            keyboard.add(detail_view_order)

        bot.send_message(
            m.chat.id, f"История заказов",
            reply_markup=keyboard, parse_mode='Markdown')

    elif m.text == '\U0001F4DDОставить оценку':
        """
        После нажатие на маркап кнопку Оставить оценку оценки и отзывы клиента сохраняется в 
        БД модель CustomerFeedback и выводится главный меню маркап кнопок (Меню, Корзина, О Нас, 
        Оформить заказ, Статус заказа, Выполненные заказы, Забронировать столик, Оценить ресторан)
        """
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                       ['\U0001F4D6\U0001F372\U0001F354Меню',
                        '\U0001F371Корзина']])
        keyboard.add(
            *[types.KeyboardButton(bot_message) for bot_message in
              ['\U0001F4DCО Нас', '\U0001F45DОформить заказ']])
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                       ['\U0001F55CСтатус заказа',
                        '\U0001F51AВыполненные заказы']])
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                       ['\U0001f6cb\ufe0fЗабронировать столик',
                        'Оценить ресторан']])

        if customer_feedback == {}:
            bot.send_message(
                m.chat.id, 'Для начало просим поставить оценки',
                reply_markup=keyboard)

        elif customer_feedback[m.from_user.id]:

            CustomerFeedback.objects.create(
                telegram_user_id_id=customer_feedback[m.from_user.id]
                ['user_id'],
                quiz_answer=customer_feedback[m.from_user.id]['quiz_answer'],
                description=customer_feedback[m.from_user.id]['text_client']
            )
            bot.send_message(
                m.chat.id, 'Спасибо за отзыв', reply_markup=keyboard)
            customer_feedback.pop(m.from_user.id)

    else:
        """
            Сохраняет отзывы клиента на временную словарь customer_feedback = {} 
        """
        for user_id in customer_feedback.keys():
            if user_id == m.from_user.id:
                customer_feedback[m.from_user.id].update(
                    {'text_client': m.text})
                print(customer_feedback)
                bot.send_message(
                    m.chat.id,
                    f"Ваша оценка: "
                    f"*{customer_feedback[m.from_user.id]['quiz_answer']}* \n"
                    f"Мнение: "
                    f"*{customer_feedback[m.from_user.id]['text_client']}* "
                    f"\n\n\n"
                    f"если согласны с оценкой нажмите "
                    f"на кнопку *\U0001F4DDОставить оценку* \n\n"
                    f"если не согласны или требуется доработка "
                    f"в оценке нажмите на *\U0001F4F5Отменить оценку*",
                    parse_mode="Markdown")


@bot.poll_answer_handler()
def handle_poll_answer(quiz_answer: types.PollAnswer):
    """
        Сохраняет оценки клиента на временную словарь customer_feedback = {}
    """
    print(quiz_answer)
    customer_feedback.update(
        {quiz_answer.user.id: {'user_id': quiz_answer.user.id,
                               'quiz_answer': quiz_answer.option_ids[0] + 1,
                               'text_client': None}})

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                   ['\U0001F4F5Отменить оценку', '\U0001F4DDОставить оценку']])
    photo = open(f"photo/Telegram-mess.jpg", 'rb')
    bot.send_photo(
        quiz_answer.user.id, photo,
        caption='Прокомментируйте, пожалуйста, Ваше мнение. \n'
                'Для этого напишите сообщением ваше пожелание. \n\n'
                'либо если не хотите писать пожелание и '
                'согласны с оценкой нажмите на кнопку '
                '*\U0001F4DDОставить оценку*, \n\n'
                'если не согласны или требуется дороботка в оценке '
                'нажмите на *\U0001F4F5Отменить оценку*',
        reply_markup=keyboard, parse_mode="Markdown")


@bot.callback_query_handler(
    func=lambda call: call.data.startswith(calendar_1_callback.prefix)
)
def callback_inline(call: CallbackQuery):
    """
        В Бронирование столиков выводит инлайн кнопки календарь (дату) и время
    """
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    global date
    date_in = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action,
        year=year, month=month, day=day
    )
    if action == "DAY":
        database.setdefault(
            call.from_user.id, {'date': date_in.strftime('%Y-%m-%d')})
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


@bot.callback_query_handler(func=lambda call: True)
def callback_inline2(call):
    """
        Обработчик обратного вызова, функция отвечает за обработку инлайн кнопок
    """
    if call.data in order(call):
        """
            Выводит детальный просмотр заказов после нажатие на инлайн кнопку 'Детальный 
            просмотр заказа №'  в маркап кнопке 'Статус заказа', в детальном просмотре 
            отображается статус заказа, продукты и итоговая сумма  
        """
        order_pk = call.data[13:]
        total_sum = 0
        if BasketToOrder.objects.filter(
                telegram_user_id_id=call.from_user.id, order__status=1,
                order=order_pk):
            bot.send_message(
                call.message.chat.id,
                f"Заказ *№{order_pk}: еще не принято в обработку*",
                parse_mode='Markdown')
        elif BasketToOrder.objects.filter(
                telegram_user_id_id=call.from_user.id, order__status=2,
                order=order_pk):
            bot.send_message(
                call.message.chat.id,
                f"Заказ *№{order_pk}: "
                f"принято в обработку*", parse_mode='Markdown')
        for basket in BasketToOrder.objects.filter(
                telegram_user_id_id=call.from_user.id, order__status__lte=2,
                order=order_pk):
            total_sum += basket.product_total_price
            bot.send_message(
                call.message.chat.id,
                f"_{basket.product.product_name}: {basket.amount}_шт. *x* "
                f"_{basket.product.price}_тг. ="
                f" _{basket.product_total_price}_ тенге",
                parse_mode='Markdown')
        bot.send_message(
            call.message.chat.id,
            f"_Итого общая сумма продукта:_ *{total_sum}* \n"
            f"_10% за обслуживание:_ *{(total_sum * 10) / 100}* \n\n"
            f"Итого общая сумма: *{((total_sum * 10) / 100) + total_sum}*",
            parse_mode='Markdown')
    if call.data in TIME:
        """
            Если выбранное время в бронирования столика находиться в константе TIME, 
            то данное время записывается на временную словарь database для дальнейшего 
            обработки данных
        """
        database[call.from_user.id]['time'] = call.data
        keyboard = InlineKeyboardMarkup(row_width=2)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Время: {call.data}",
            reply_markup=get_persons(keyboard)
        )
    if call.data in PERSONS:
        """
            Если выбранное количество людей в бронирования столика находиться в константе PERSONS, 
            то данные записывается на временную словарь database для дальнейшего 
            обработки данных
        """
        database[call.from_user.id]['persons'] = call.data
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                       ['Изменить бронь', 'Бронировать', 'Вернуться в меню']])
        bot.send_message(
            chat_id=call.from_user.id,
            text=f'''Дата: {database[call.from_user.id]['date']},
                     время: {database[call.from_user.id]['time']},
                     количество людей: {database[call.from_user.id]['persons']}
            Изменить данные или продолжить?''',
            reply_markup=keyboard,
        )
    if call.data == 'order_processing':
        """
            После нажатие на инлайн кнопку «Оформить заказ» в базе модель «StatusShoppingCartOrder» 
            создается заказ с следующими параметрами (№заказа, телеграммID, дата создание), после все 
            продукты с временного базы модель «Basket» переносится на постоянную базу модель «BasketToOrder» 
            с добавлением параметра заказа (т.е. ID заказа). Следом телеграмм боту мерчанта отправляется 
            уведомление с инлайн кнопкой, в инлайн кнопке указывается ссылка на созданную заказ.
        """
        for status in StatusShoppingCartOrder.objects.all():
            if status.status == 'Новый':
                new_status = status
        shopping_cart_orders = ShoppingCartOrder.objects.create(
            telegram_user_id_id=call.from_user.id,
            status=new_status
        )
        total_sum = 0
        for menu in response_menu:

            for basket in Basket.objects.filter(
                    telegram_user_id_id=call.from_user.id):
                if Basket.objects.filter(
                        product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id):
                    BasketToOrder.objects.create(
                        product=basket.product,
                        telegram_user_id=basket.telegram_user_id,
                        amount=basket.amount,
                        product_total_price=basket.product_total_price,
                        status=basket.status,
                        order=shopping_cart_orders
                    )
                    basket.delete()
                    total_sum += basket.product_total_price

        bot.send_message(
            call.message.chat.id,
            f"*Заказ №{shopping_cart_orders.id} в обработке* \n"
            f"_Итого общая сумма продукта:_ *{total_sum}* \n"
            f"_10% за обслуживание:_ *{(total_sum * 10) / 100}* \n\n"
            f"Итого общая сумма: *{((total_sum * 10) / 100) + total_sum}*",
            parse_mode='Markdown')
        for users in MerchantTelegramUser.objects.all():
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton(
                    text=f"Перейти к заказу №{shopping_cart_orders.id}",
                    url=f"{url_crm}/order/"
                        f"{shopping_cart_orders.id}"))

            merchant_bot.send_message(
                users.user_id,
                f'поступил заказ с номером *№{shopping_cart_orders.id}* \n'
                f'сумма заказа *{((total_sum * 10) / 100) + total_sum}* тенге',
                reply_markup=keyboard, parse_mode='Markdown')

    elif call.data == '\U0001F45DОформить заказ':
        """
        
        """
        if not Basket.objects.filter(
                telegram_user_id_id=call.from_user.id):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                types.InlineKeyboardButton(
                    text='\U0001F4D6\U0001F372\U0001F354Меню',
                    callback_data='\U0001F4D6\U0001F372\U0001F354Меню'))
            bot.send_message(
                call.chat.id, f"_Заказ не можем создать, "
                              f"для начала выберите блюд из_ *Меню*  \n",
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
                if basket.telegram_user_id_id == call.from_user.id:
                    total_sum += basket.product_total_price
                    bot.send_message(
                        call.message.chat.id,
                        f"*{basket.product.product_name}:"
                        f"* *{basket.amount}*шт. *x* "
                        f"*{basket.product.price}*тг. = "
                        f"*{basket.product_total_price}* тенге",
                        parse_mode='Markdown')
            bot.send_message(
                call.message.chat.id,
                f"_Итого общая сумма продукта:_ *{total_sum}* \n"
                f"_10% за обслуживание:_ *{(total_sum * 10) / 100}* \n\n"
                f"Итого общая сумма: *{((total_sum * 10) / 100) + total_sum}*",
                reply_markup=keyboard, parse_mode='Markdown')
    if call.data[:16] == f'completed_orders':
        if BasketToOrder.objects.filter(telegram_user_id_id=call.from_user.id, order_id=int(call.data[16:])):
            pdf = FPDF(orientation='P', unit='mm', format='A5')
            pdf.add_page()
            pdf.add_font('DejaVu', '', fname='font/DejaVuSansCondensed.ttf', uni=True)
            pdf.set_font('DejaVu', '', 20)
            # pdf.set_text_color(255, 0, 0)
            pdf.cell(120, 10,
                     txt=f'Заказ №{call.data[16:]}',
                     ln=1, align="C")
            pdf.ln(6)
            pdf.set_line_width(0.4)
            pdf.set_draw_color(255, 0, 0)
            pdf.line(20, 20, 130, 20)
            total_sum = 0
            for baskets in BasketToOrder.objects.filter(
                    telegram_user_id_id=call.from_user.id, order_id=int(call.data[16:])
            ):
                total_sum += baskets.product_total_price
                pdf.set_font('DejaVu', '', 12)
                pdf.set_text_color(0, 0, 255)
                pdf.cell(110, 10,
                         txt=f'{baskets.product.product_name}: {baskets.product.price} тг. x '
                             f'{baskets.amount} шт. = {baskets.product_total_price} тенге',
                         ln=1, align="C")
                print(f'{baskets.product.product_name}: {baskets.product.price} тг. x '
                      f'{baskets.amount} шт. = {baskets.product_total_price} тенге')

            pdf.set_font('DejaVu', '', 13)
            pdf.ln(6)
            pdf.cell(110, 10, txt=f'Сумма {total_sum} тенге', ln=1, align="C")
            pdf.cell(110, 10, txt=f'10% за обслуживание {(total_sum * 10) / 100} тенге', ln=1, align="C")
            pdf.cell(110, 10, txt=f'Итоговая сумма {total_sum + (total_sum * 10) / 100} тенге', ln=1, align="C")

            pdf.output(f"PDF/{call.data[16:]}-{call.from_user.id}.pdf")

        doc = open(f"PDF/{call.data[16:]}-{call.from_user.id}.pdf", 'rb')
        bot.send_document(call.message.chat.id, doc)
        os.remove(f"PDF/{call.data[16:]}-{call.from_user.id}.pdf")

    if call.data != '\U0001F4D6\U0001F372\U0001F354Меню':
        for menu in response_menu:
            if call.data == menu['category']:
                for response_category in response_categories:
                    if menu['category'] == response_category['category_name'] \
                            and menu['available'] == 'Есть':
                        keyboard = types.InlineKeyboardMarkup(row_width=2)

                        print(menu['photo'][1:])

                        photo = open(menu['photo'][1:], 'rb')

                        if not Basket.objects.filter(
                                product_id=menu['id'],
                                telegram_user_id_id=call.from_user.id):
                            add_menu = types.InlineKeyboardButton(
                                text=f"\U00002795\U0001F371"
                                     f"Добавить в корзину",
                                callback_data=f"add_menu_{menu['id']}")

                            keyboard.add(add_menu)

                            bot.send_photo(
                                call.message.chat.id, photo,
                                caption=text_menu(menu), reply_markup=keyboard,
                                parse_mode="Markdown")

                        elif Basket.objects.filter(
                                product_id=menu['id'],
                                telegram_user_id_id=call.from_user.id):
                            basket = get_object_or_404(
                                Basket, product_id=menu['id'],
                                telegram_user_id_id=call.from_user.id)

                            button_menu(keyboard, basket)

                            bot.send_photo(
                                call.message.chat.id, photo,
                                caption=text_basket(basket),
                                reply_markup=keyboard, parse_mode="Markdown")

            elif call.data == f"add_menu_{menu['id']}":
                if not Basket.objects.filter(
                        product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id):
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    basket = Basket.objects.create(
                        amount=1,
                        product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id,
                        product_total_price=menu['price'],
                    )

                    button_menu(keyboard, basket)

                    bot.edit_message_caption(
                        caption=text_basket(basket),
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        reply_markup=keyboard, parse_mode="Markdown")

                    bot.answer_callback_query(
                        callback_query_id=call.id, show_alert=False,
                        text=f'"{basket.product.product_name}" '
                             f'добавлено в корзину '
                             f'\n Общая количество 1')

                elif Basket.objects.filter(
                        product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id):
                    keyboard = types.InlineKeyboardMarkup(row_width=2)

                    basket = get_object_or_404(
                        Basket, product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id)
                    add_meals(basket, menu)

                    button_menu(keyboard, basket)

                    bot.edit_message_caption(
                        caption=text_basket(basket),
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        reply_markup=keyboard, parse_mode="Markdown")
                    bot.answer_callback_query(
                        callback_query_id=call.id, show_alert=False,
                        text=f'"{basket.product.product_name}" '
                             f'добавлено в корзину '
                             f'\n Общая количество {basket.amount}')

            elif call.data == f"subtract_menu_{menu['id']}":
                for telegram_user in TelegramUser.objects.all():
                    if call.from_user.id == telegram_user.user_id:
                        if Basket.objects.filter(
                                amount__gt=1, product_id=menu['id'],
                                telegram_user_id_id=telegram_user.user_id):
                            keyboard = types.InlineKeyboardMarkup(row_width=2)

                            basket = get_object_or_404(
                                Basket, product_id=menu['id'],
                                telegram_user_id_id=telegram_user.user_id)
                            subtract_meals(basket, menu)
                            button_menu(keyboard, basket)
                            bot.answer_callback_query(
                                callback_query_id=call.id, show_alert=False,
                                text=f'"{basket.product.product_name}" '
                                     f'удалено с корзины '
                                     f'\n Общая количество {basket.amount}')
                            bot.edit_message_caption(
                                caption=text_basket(basket),
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=keyboard, parse_mode="Markdown")

                        elif Basket.objects.filter(
                                amount=1, product_id=menu['id'],
                                telegram_user_id_id=telegram_user.user_id):
                            basket = Basket.objects.filter(
                                amount=1, product_id=menu['id'],
                                telegram_user_id_id=call.from_user.id)
                            product = get_object_or_404(
                                Basket, product_id=menu['id'],
                                telegram_user_id_id=telegram_user.user_id)
                            basket.delete()

                            keyboard = types.InlineKeyboardMarkup(row_width=2)
                            add_menu = types.InlineKeyboardButton(
                                text=f"\U00002795\U0001F371"
                                     f"Добавить в корзину",
                                callback_data=f"add_menu_{menu['id']}")
                            keyboard.add(add_menu)
                            bot.answer_callback_query(
                                callback_query_id=call.id, show_alert=False,
                                text=f'"{product.product.product_name}" '
                                     f'удалено с корзины')
                            bot.edit_message_caption(
                                caption=text_menu(menu),
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=keyboard, parse_mode="Markdown")

            elif call.data == f"add_basket_{menu['id']}":
                if not Basket.objects.filter(
                        product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id):
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    basket = Basket.objects.create(
                        amount=1,
                        product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id,
                        product_total_price=menu['price'],
                    )
                    button_basket(keyboard, basket)

                    bot.edit_message_caption(
                        caption=text_basket(basket),
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        reply_markup=keyboard, parse_mode="Markdown")

                    bot.answer_callback_query(
                        callback_query_id=call.id, show_alert=False,
                        text=f'"{basket.product.product_name}" '
                             f'добавлено в корзину '
                             f'\n Общая количество 1')

                elif Basket.objects.filter(
                        product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id):
                    keyboard = types.InlineKeyboardMarkup(row_width=2)

                    basket = get_object_or_404(
                        Basket, product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id)
                    add_meals(basket, menu)

                    button_basket(keyboard, basket)

                    bot.edit_message_caption(
                        caption=text_basket(basket),
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        reply_markup=keyboard, parse_mode="Markdown")

                    bot.answer_callback_query(
                        callback_query_id=call.id, show_alert=False,
                        text=f'"{basket.product.product_name}" '
                             f'добавлено в корзину '
                             f'\n Общая количество {basket.amount}')

            elif call.data == f"subtract_basket_{menu['id']}":
                if Basket.objects.filter(
                        amount__gt=1, product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id):
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    basket = get_object_or_404(
                        Basket, product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id)
                    subtract_meals(basket, menu)

                    button_basket(keyboard, basket)

                    bot.edit_message_caption(
                        caption=text_basket(basket),
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        reply_markup=keyboard, parse_mode="Markdown")
                    bot.answer_callback_query(
                        callback_query_id=call.id, show_alert=False,
                        text=f'"{basket.product.product_name}" '
                             f'удалено с корзины '
                             f'\n Общая количество {basket.amount}')

                elif Basket.objects.filter(
                        amount=1, product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id):
                    basket = Basket.objects.filter(
                        amount=1, product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id)
                    product = get_object_or_404(
                        Basket, product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id)
                    basket.delete()
                    bot.answer_callback_query(
                        callback_query_id=call.id, show_alert=False,
                        text=f'"{product.product.product_name}" '
                             f'удалено с корзины')
                    bot.delete_message(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id, timeout=1)
                    if not Basket.objects.filter(
                            telegram_user_id_id=call.from_user.id):
                        keyboard = types.InlineKeyboardMarkup(row_width=1)
                        keyboard.add(types.InlineKeyboardButton(
                            text='\U0001F4D6\U0001F372\U0001F354Меню',
                            callback_data='\U0001F4D6\U0001F372\U0001F354'
                                          'Меню'))
                        bot.send_message(
                            call.message.chat.id,
                            '_Корзина пуста, для добавление '
                            'перейдите в_ *Меню* ',
                            reply_markup=keyboard, parse_mode='Markdown')

            elif call.data == 'edit_basket':
                if Basket.objects.filter(
                        product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id):
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    basket = get_object_or_404(
                        Basket, product_id=menu['id'],
                        telegram_user_id_id=call.from_user.id)

                    print(f"uploads/{basket.product.photo}")

                    photo = open(f"uploads/{basket.product.photo}", 'rb')

                    button_basket(keyboard, basket)
                    bot.send_photo(
                        call.message.chat.id, photo,
                        caption=text_basket(basket),
                        reply_markup=keyboard, parse_mode="Markdown")

                if not Basket.objects.filter(
                        telegram_user_id_id=call.from_user.id):
                    keyboard = types.InlineKeyboardMarkup(row_width=1)
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text='\U0001F4D6\U0001F372\U0001F354'
                                 'Меню',
                            callback_data='\U0001F4D6\U0001F372\U0001F354'
                                          'Меню'))
                    bot.send_message(
                        call.message.chat.id,
                        '<i>Корзина пуста, перейдите в</i> '
                        '<ins><b>Меню</b></ins>'
                        ' <i>для заказа блюд</i>',
                        reply_markup=keyboard, parse_mode="HTML")

    elif call.data == '\U0001F4D6\U0001F372\U0001F354Меню':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for api_category in response_categories:
            category = types.InlineKeyboardButton(
                text=f"{api_category['category_name']}-"
                     f"\U0001F355\U0001F354\U0001F379\U0001F382",
                callback_data=f"{api_category['category_name']}")
            keyboard.add(category)
        bot.send_message(
            call.message.chat.id,
            'Категории\U0001F4C4\U0001F355\U0001F354\U0001F379\U0001F382',
            reply_markup=keyboard, parse_mode="Markdown")


if __name__ == '__main__':
    bot.polling(none_stop=True)
    while True:
        time.sleep(200000)

# bot.polling(none_stop=True, interval=0)
# merchant_bot.polling(none_stop=True, interval=0)
