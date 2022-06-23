from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView
from rest_framework.reverse import reverse_lazy

from product.models import TableReservation
import telebot


client_key = '5388600014:AAHFGhuoNaXEK7dcd-qRi0okx-Wa2S5Gs2U'
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
        bot.send_message(self.object.telegram_user_id,
                         f'Ваша бронь: Стол №{self.object.table_number}: {self.object.date}, {self.object.time}',
                         parse_mode='Markdown')
        self.object.save()
        return redirect('reserv_list')


class TableReservationDeleteView(DeleteView):
    model = TableReservation
    success_url = reverse_lazy('reserv_list')

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(self.model, pk=kwargs.get('pk'))
        bot.send_message(user.telegram_user_id,
                         f'Ваша бронь на дату {user.date} и время {user.time}. Отменили',
                         parse_mode='Markdown')
        return self.delete(request=request)
