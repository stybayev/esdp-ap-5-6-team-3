from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.views.generic import UpdateView, DeleteView
from rest_framework.reverse import reverse_lazy
from product.forms import TableReservationForm, SearchForm
from product.helpers import SearchView
from product.models import TableReservation
import telebot


client_key = '5388600014:AAHFGhuoNaXEK7dcd-qRi0okx-Wa2S5Gs2U'
bot = telebot.TeleBot(client_key)


class ReservationListView(SearchView):
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


class ReservationTableEditView(UpdateView):
    template_name = 'table/table_reservation_list.html'
    model = TableReservation

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model, pk=kwargs.get('pk'))
        self.object.status = 'Выполнено'
        self.object.table_number = request.POST.get('table_number')
        bot.send_message(self.object.telegram_user_id_id,
            f'Ваша бронь: Стол №{self.object.table_number}, дата: {self.object.date}, время:{self.object.time}',
                         parse_mode='Markdown')
        self.object.save()
        return redirect('reserve_list', status='Новый')


class TableReservationDeleteView(DeleteView):
    model = TableReservation

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(self.model, pk=kwargs.get('pk'))
        bot.send_message(user.telegram_user_id_id,
        f'Бронь на дату {user.date} и время {user.time} отменили. Если у вас возникли вопросы свяжитесь с менеджером',
                         parse_mode='Markdown')
        return self.delete(request=request)

    def get_success_url(self):
        return reverse('reserve_list', kwargs={'status': self.object.status})


class ReservationTableUpdateView(UpdateView):
    template_name = 'table/table_update.html'
    model = TableReservation
    form_class = TableReservationForm

    def get_success_url(self):
        return reverse('reserve_list', kwargs={'status': self.object.status})
