from django.contrib.auth.mixins import LoginRequiredMixin

from config import client_key
from django.db.models import Q
from product.forms import SearchForm
from product.helpers import SearchView
from product.models import ShoppingCartOrder
from django.views.generic import DetailView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
import telebot
from product.services import order_change_status, cancel_order

bot = telebot.TeleBot(client_key)


class OrderListView(LoginRequiredMixin, SearchView):
    """
        View для просмотра списка 'Заказов'
    """
    template_name = 'order/list_order_view.html'
    model = ShoppingCartOrder
    ordering = ("updated_at",)
    paginate_by = 10
    paginate_orphans = 1
    context_object_name = 'orders'
    search_form = SearchForm
    search_fields = {
        'telegram_user_id__first_name': 'icontains',
        'telegram_user_id__last_name': 'icontains',
        'id': 'icontains'
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.kwargs.get('status')
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(
            status__status=self.kwargs.get('status'))
        if self.search_value:
            query = Q()
            query_list = [
                Q(**{f"{key}__{value}": self.search_value})
                for key, value in self.search_fields.items()
            ]
            for query_part in query_list:
                query = (query | query_part)
            queryset = queryset.filter(query)
        return queryset


class OrderDetailView(LoginRequiredMixin, DetailView):
    """
        View для детального просмотра записи 'Заказа'
    """
    template_name = 'order/detail_order_view.html'
    model = ShoppingCartOrder
    context_object_name = 'order'


class OrderChangeStatusView(LoginRequiredMixin, TemplateView):
    """
        View для изменения статуса 'Заказа' через кнопки
    """
    template_name = 'order/detail_order_view.html'
    order = None

    def get_success_url(self):
        return reverse('orders_view',
                       kwargs={'status': self.order.status.status})

    def post(self, request, *args, **kwargs):
        order_object = get_object_or_404(ShoppingCartOrder,
                                         pk=kwargs.get('pk'))
        self.order = order_change_status(request.POST, order_object)
        return redirect(self.get_success_url())


class CancelOrder(TemplateView):
    """
        View для возврата 'Заказа'
    """
    order = None

    def get_success_url(self):
        return reverse('orders_view',
                       kwargs={'status': 'Новый'})

    def post(self, request, *args, **kwargs):
        order_object = get_object_or_404(ShoppingCartOrder,
                                         pk=kwargs.get('pk'))
        self.order = cancel_order(request.POST, order_object)
        return redirect(self.get_success_url())
