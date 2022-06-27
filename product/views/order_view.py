from config import client_key
from product.forms import SearchForm
from product.helpers import SearchView
from product.models import ShoppingCartOrder, StatusShoppingCartOrder, \
    Basket
from django.views.generic import DetailView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
import telebot
from telebot import types


bot = telebot.TeleBot(client_key)


class OrderListView(SearchView):
    template_name = 'order/list_order_view.html'
    model = ShoppingCartOrder
    ordering = ("updated_at",)
    context_object_name = 'orders'
    search_form = SearchForm
    search_fields = {
        'telegram_user_id__first_name': 'icontains',
        'telegram_user_id__last_name': 'icontains',
        'id': 'icontains'
    }


class OrderDetailView(DetailView):
    template_name = 'order/detail_order_view.html'
    model = ShoppingCartOrder
    context_object_name = 'order'


class OrderChangeStatusView(TemplateView):
    template_name = 'order/detail_order_view.html'

    def get_success_url(self):
        return reverse('orders_view')

    def post(self, request, *args, **kwargs):
        current_status = request.POST.get('status')
        telegram_user_id = request.POST.get('telegram_user_id')
        order_pk = kwargs.get('pk')
        order = get_object_or_404(ShoppingCartOrder, pk=order_pk)
        statuses = StatusShoppingCartOrder.objects.all()
        for status in statuses:
            if status.status == current_status:
                order.status = status
                order.save()
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                detail_view_order = types.InlineKeyboardButton(
                    text=f"Детальный просмотр заказа №{order_pk} \n",
                    callback_data=f'order_detail_{order_pk}')
                keyboard.add(detail_view_order)
                if order.status_id == 2:
                    bot.send_message(telegram_user_id,
                                     f"Заказ *№{order_pk}* "
                                     f"принята мерчантом в обработку \n ",
                                     reply_markup=keyboard,
                                     parse_mode='Markdown')
                elif order.status_id == 3:
                    bot.send_message(telegram_user_id,
                                     f"Заказ *№{order_pk}* заверщен \n"
                                     f"Заказ перенесен в *Истории заказов*",
                                     parse_mode='Markdown')
        return redirect(self.get_success_url())


class CancelOrder(TemplateView):
    def get_success_url(self):
        return reverse('orders_view')

    def post(self, request, *args, **kwargs):
        order_pk = kwargs.get('pk')
        order = get_object_or_404(ShoppingCartOrder, pk=order_pk)
        telegram_user_id = request.POST.get('telegram_user_id')
        for ord_bask in order.basket_order.all():
            basket = Basket.objects.create(
                product=ord_bask.product,
                telegram_user_id=ord_bask.telegram_user_id,
                amount=ord_bask.amount,
                product_total_price=ord_bask.product_total_price,
            )
            if basket.product.available == 'Нет':
                bot.send_message(telegram_user_id,
                                 f"Заказ *№{order_pk}* "
                                 f"возвращен в *Корзину* \n"
                                 f"закончился *{basket.product.product_name}*",
                                 parse_mode='Markdown')
            else:
                bot.send_message(telegram_user_id,
                                 f"Заказ *№{order_pk}* "
                                 f"возвращен в *Корзину* \n"
                                 f"для уточнение просим обратиться к Мерчанту",
                                 parse_mode='Markdown')
        order.delete()

        return redirect(self.get_success_url())
