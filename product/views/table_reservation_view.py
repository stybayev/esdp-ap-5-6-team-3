from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.views.generic import ListView, UpdateView, DeleteView
from rest_framework.reverse import reverse_lazy
from product.forms import TableReservationForm
from product.models import TableReservation
import telebot


client_key = '5364245042:AAFrhGGJjLitrjAubUocJfrzTHkegtuMxIg'
bot = telebot.TeleBot(client_key)


class ReservationListView(ListView):
    template_name = 'table/table_reservation_list.html'
    model = TableReservation
    context_object_name = 'reservations'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = TableReservation.TABLE_NUMBERS
        return context


class ReservationTableEditView(UpdateView):
    template_name = 'table/table_reservation_list.html'
    model = TableReservation

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model, pk=kwargs.get('pk'))
        self.object.status = 'Выполнено'
        self.object.table_number = request.POST.get('table_number')
        print(request.POST)
        bot.send_message(self.object.telegram_user_id_id,
            f'Ваша бронь: Стол №{self.object.table_number}, дата: {self.object.date}, время:{self.object.time}',
                         parse_mode='Markdown')
        self.object.save()
        return redirect('reserve_list')


class TableReservationDeleteView(DeleteView):
    model = TableReservation
    success_url = reverse_lazy('reserve_list')

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(self.model, pk=kwargs.get('pk'))
        bot.send_message(user.telegram_user_id_id,
        f'Бронь на дату {user.date} и время {user.time} отменили. Если у вас возникли вопросы свяжитесь с менеджером',
                         parse_mode='Markdown')
        return self.delete(request=request)


class ReservationTableUpdateView(UpdateView):
    template_name = 'table/table_update.html'
    model = TableReservation
    form_class = TableReservationForm

    def get_success_url(self):
        return reverse('reserve_list')
