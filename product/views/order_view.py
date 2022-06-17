from product.forms import SearchForm, ChangeOrderStatusForm
from product.helpers import SearchView
from product.models import ShoppingCartOrder, ShoppingCartOrderBasketToOrder, BasketToOrder, StatusShoppingCartOrder, \
    Basket
from django.views.generic import DetailView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse


class OrderListView(SearchView):
    template_name = 'order/list_order_view.html'
    model = ShoppingCartOrder
    ordering = ("updated_at",)
    context_object_name = 'orders'
    paginate_by = 10
    paginate_orphans = 1
    search_form = SearchForm
    search_fields = {
        'category_name': 'icontains',
        'translit_category_name': 'icontains',
        'category_name_translation': 'icontains'
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
        order = get_object_or_404(ShoppingCartOrder, pk=kwargs.get('pk'))
        statuses = StatusShoppingCartOrder.objects.all()
        for status in statuses:
            if status.status == current_status:
                order.status = status
                order.save()
        return redirect(self.get_success_url())


class CancelOrder(TemplateView):
    def get_success_url(self):
        return reverse('orders_view')

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(ShoppingCartOrder, pk=kwargs.get('pk'))
        for ord_bask in order.basket_order.all():
            Basket.objects.create(
                product=ord_bask.product,
                telegram_user_id=ord_bask.telegram_user_id,
                amount=ord_bask.amount,
                product_total_price=ord_bask.product_total_price,
            )
        order.delete()
        return redirect(self.get_success_url())
