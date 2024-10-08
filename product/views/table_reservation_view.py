from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, reverse
from django.views.generic import UpdateView, DeleteView
from config import client_key
from product.forms import TableReservationForm, SearchForm
from product.helpers import SearchView
from product.models import TableReservation
import telebot
from product.services import table_reservation_accept

bot = telebot.TeleBot(client_key)


class ReservationListView(LoginRequiredMixin, SearchView):
    """
        View для просмотра списка записей 'Бронирования столиков'
    """
    template_name = 'table/table_reservation_list.html'
    model = TableReservation
    context_object_name = 'reservations'
    paginate_by = 10
    ordering = ['-created_at', '-updated_at']
    paginate_orphans = 1
    search_form = SearchForm
    search_fields = {
        'telegram_user_id__first_name': 'icontains',
        'telegram_user_id__last_name': 'icontains',
        'id': 'icontains'
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.kwargs.get('status')
        context['table'] = TableReservation.TABLE_NUMBERS
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(status=self.kwargs.get('status'))
        if self.search_value:
            query = Q()
            query_list = [
                Q(**{f"{key}__{value}": self.search_value})
                for key, value in self.search_fields.items()
            ]
            for query_part in query_list:
                query = (query | query_part)
            queryset = queryset.filter(query)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class ReservationTableEditView(LoginRequiredMixin, UpdateView):
    """
        View для потверждения 'Бронирования столиков'
    """
    template_name = 'table/table_reservation_list.html'
    model = TableReservation

    def post(self, request, *args, **kwargs):
        reservation = get_object_or_404(self.model, pk=kwargs.get('pk'))
        table_reservation_accept(request.POST, reservation)
        return redirect('reserve_list', status='Новый')


class TableReservationDeleteView(LoginRequiredMixin, DeleteView):
    """
        View для отмены 'Бронирования столиков'
    """
    model = TableReservation

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(self.model, pk=kwargs.get('pk'))
        bot.send_message(user.telegram_user_id_id,
                         f'Бронь на дату {user.date} и '
                         f'время {user.time} отменили. '
                         f'Если у вас возникли вопросы свяжитесь с менеджером',
                         parse_mode='Markdown')
        return self.delete(request=request)

    def get_success_url(self):
        return reverse('reserve_list', kwargs={'status': self.object.status})


class ReservationTableUpdateView(LoginRequiredMixin, UpdateView):
    """
        View для изменения записи 'Бронирования столиков'
    """
    template_name = 'table/table_update.html'
    model = TableReservation
    form_class = TableReservationForm

    def get_success_url(self):
        return reverse('reserve_list', kwargs={'status': self.object.status})
