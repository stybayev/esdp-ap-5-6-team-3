from product.forms import SearchForm, ChangeOrderStatusForm
from product.helpers import SearchView
from product.models import ShoppingCartOrder, ShoppingCartOrderBasketToOrder, BasketToOrder
from django.views.generic import UpdateView, DetailView
from django.urls import reverse_lazy


class OrderListView(SearchView):
    template_name = 'order/list_order_view.html'
    model = ShoppingCartOrder
    ordering = ("updated_at",)
    context_object_name = 'orders'
    paginate_by = 10
    paginate_orphans = 1
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


class OrderChangeStatusView(UpdateView):
    template_name = 'order/update_order_status_view.html'
    form_class = ChangeOrderStatusForm
    model = ShoppingCartOrder
    context_object_name = 'order'
    success_url = reverse_lazy('orders_view')

