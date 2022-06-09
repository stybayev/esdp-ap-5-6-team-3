from product.forms import SearchForm
from product.helpers import SearchView
from product.models import ShoppingCartOrderBasketToOrder


class OrderListView(SearchView):
    template_name = 'order/list_order_view.html'
    model = ShoppingCartOrderBasketToOrder
    ordering = ("id",)
    context_object_name = 'orders'
    paginate_by = 10
    paginate_orphans = 1
    search_form = SearchForm
    search_fields = {
        'category_name': 'icontains',
        'translit_category_name': 'icontains',
        'category_name_translation': 'icontains'
    }