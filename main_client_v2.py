import django
import os
from django.shortcuts import get_object_or_404
from telegram import InputFile

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()
import telebot
from telebot import types
from requests import get
import time
from product.models import TelegramUser, Product, Basket, Aboutus, Category

bot = telebot.TeleBot('5388600014:AAHFGhuoNaXEK7dcd-qRi0okx-Wa2S5Gs2U')
print(time.ctime())
time.sleep(3)

url_menu = 'http://localhost:8000/api/v1/menu/'
url_category = 'http://localhost:8000/api/v1/category/'

response_menu = get(url_menu).json()
response_categories = get(url_category).json()


def text_basket(basket):
    basket_text = (f"_Наименование_: *{basket.product.id}-{basket.product.product_name}* \n"
                   f"_Цена_: *{basket.product.price}* тенге \n"
                   f"_Категория_: *{basket.product.category}* \n"
                   f"_Описание_: *{basket.product.description}* \n\n"
                   f"*В корзине* \n"
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
    category = types.InlineKeyboardButton(
        text=f"Назад в категории {basket.product.category}",
        callback_data=f"{basket.product.category}")
    keyboard.add(add_menu, subtract_menu, category)


@bot.message_handler(commands=["start"])
def start(m):
    print(type(m.from_user.id))

    if TelegramUser.objects.filter(user_id=m.from_user.id):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        msg = bot.send_message(m.chat.id, f'Приветствую Вас *{m.from_user.first_name}*!', reply_markup=keyboard,
                               parse_mode="Markdown")
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in
                       ['\U0001F4D6\U0001F372\U0001F354Меню', '\U0001F371Корзина']])
        keyboard.add(*[types.KeyboardButton(bot_message) for bot_message in ['\U0001F4DCО Нас']])

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

    elif m.text == '\U0001F371Корзина':
        for basket in Basket.objects.all():
            if m.from_user.id == basket.telegram_user_id_id:
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                print(f"uploads/{basket.product.photo}")
                photo = open(f"uploads/{basket.product.photo}", 'rb')
                button_basket(keyboard, basket)
                bot.send_photo(m.chat.id, photo, caption=text_basket(basket), reply_markup=keyboard,
                               parse_mode="Markdown")

        if not Basket.objects.filter(telegram_user_id_id=m.from_user.id):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(types.InlineKeyboardButton(text='\U0001F4D6\U0001F372\U0001F354Меню',
                                                    callback_data='\U0001F4D6\U0001F372\U0001F354Меню'))
            bot.send_message(m.chat.id,
                             '<i>Корзина пуста, перейдите в</i> <ins><b>Меню</b></ins> <i>для заказа блюд</i>',
                             reply_markup=keyboard, parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data != '\U0001F4D6\U0001F372\U0001F354Меню':
        for menu in response_menu:

            if call.data == menu['category']:
                keyboard = types.InlineKeyboardMarkup(row_width=2)

                if Category.objects.filter(category_name=menu['category']):

                    add_menu = types.InlineKeyboardButton(
                        text=f"Детальный просмотр-{menu['product_name']}",
                        callback_data=f"detailed_{menu['id']}")
                    keyboard.add(add_menu)

                bot.send_message(call.message.chat.id, f"*{menu['category']}, {menu['product_name']} "
                                                       f"Цена: {menu['price']} тенге*",
                                 reply_markup=keyboard, parse_mode="Markdown")

            elif call.data == f"detailed_{menu['id']}":
                # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id, timeout=1)
                keyboard = types.InlineKeyboardMarkup(row_width=2)

                print(menu['photo'][1:])

                photo = open(menu['photo'][1:], 'rb')
                if not Basket.objects.filter(product_id=menu['id'], telegram_user_id_id=call.from_user.id):
                    add_menu = types.InlineKeyboardButton(
                        text=f"\U00002795\U0001F371Добавить в корзину",
                        callback_data=f"add_menu_{menu['id']}")
                    category = types.InlineKeyboardButton(
                        text=f"Назад в категории {menu['category']}",
                        callback_data=f"{menu['category']}")

                    keyboard.add(add_menu, category)

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
                if Basket.objects.filter(amount__gt=1, product_id=menu['id'], telegram_user_id_id=call.from_user.id):
                    keyboard = types.InlineKeyboardMarkup(row_width=2)

                    basket = get_object_or_404(Basket, product_id=menu['id'], telegram_user_id_id=call.from_user.id)

                    subtract_meals(basket, menu)

                    button_menu(keyboard, basket)
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text=f'"{basket.product.product_name}" удалено с корзины \n Общая количество {basket.amount}')
                    bot.edit_message_caption(caption=text_basket(basket), chat_id=call.message.chat.id,
                                             message_id=call.message.message_id,
                                             reply_markup=keyboard, parse_mode="Markdown")

                elif Basket.objects.filter(amount=1, product_id=menu['id'], telegram_user_id_id=call.from_user.id):
                    basket = Basket.objects.filter(amount=1, product_id=menu['id'], telegram_user_id_id=call.from_user.id)
                    product = get_object_or_404(Basket, product_id=menu['id'], telegram_user_id_id=call.from_user.id)
                    basket.delete()

                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    add_menu = types.InlineKeyboardButton(
                        text=f"\U00002795\U0001F371Добавить в корзину",
                        callback_data=f"add_menu_{menu['id']}")
                    category = types.InlineKeyboardButton(
                        text=f"Назад в категории {menu['category']}",
                        callback_data=f"{menu['category']}")

                    keyboard.add(add_menu, category)
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
                    basket = Basket.objects.filter(amount=1, product_id=menu['id'], telegram_user_id_id=call.from_user.id)
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
