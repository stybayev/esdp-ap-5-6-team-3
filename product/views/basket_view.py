from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView

from product.models import Product, Basket, BasketStatus, TelegramUser
from product.forms import SearchForm
from product.helpers import SearchView


class BasketProductListView(SearchView):
    template_name = 'basket/list_basket_menu_view.html'
    model = Product
    queryset = Product.objects.filter(available='Есть')
    ordering = ("created_at",)
    context_object_name = 'products'
    paginate_by = 5
    paginate_orphans = 1
    search_form = SearchForm
    search_fields = {
        'product_name': 'icontains',
        'description': 'icontains',
        'category__category_name': 'icontains',
        'price': 'icontains',
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['total_baskets'] = Basket.objects.all()
        return context


class BasketListView(SearchView):
    template_name = 'basket/list_basket_view.html'
    model = Basket
    ordering = ("id",)
    context_object_name = 'baskets'
    paginate_by = 5
    paginate_orphans = 1
    search_form = SearchForm
    search_fields = {
        'product__product_name': 'icontains',
        'amount': 'icontains',
        'product_total_price': 'icontains',
        'status': 'icontains',
    }

    def telegram_user(self):
        for user in TelegramUser.objects.all():
            return user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['total_baskets'] = Basket.objects.all()
        return context


class AddBasketView(CreateView):
    model = Basket

    def telegram_user(self):
        for user in TelegramUser.objects.all():
            return user

    def post(self, request, *args, **kwargs):
        product_pk = kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_pk)
        print(product, product_pk)
        if not self.model.objects.filter(product_id=product_pk, telegram_user_id_id=self.telegram_user().user_id):
            self.model.objects.create(
                amount=1,
                product_id=product_pk,
                telegram_user_id_id=self.telegram_user().user_id,
                product_total_price=product.price,
            )
        elif self.model.objects.filter(product_id=product_pk, telegram_user_id_id=self.telegram_user().user_id):
            basket = get_object_or_404(self.model, product_id=product_pk, telegram_user_id_id=self.telegram_user().user_id)
            basket.amount += 1
            basket.product_total_price += product.price
            basket.save()
        return redirect(request.META.get('HTTP_REFERER'))


class SubtractBasketView(CreateView):
    model = Basket

    def telegram_user(self):
        for user in TelegramUser.objects.all():
            return user

    def post(self, request, *args, **kwargs):
        product_pk = kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_pk)
        if self.model.objects.filter(amount__gt=1, product_id=product_pk):
            basket = get_object_or_404(self.model, product_id=product_pk, telegram_user_id_id=self.telegram_user().user_id)
            basket.amount -= 1
            basket.product_total_price -= product.price
            basket.save()
        elif self.model.objects.filter(amount=1, product_id=product_pk):
            basket = self.model.objects.filter(amount=1, product_id=product_pk)
            basket.delete()
        return redirect(request.META.get('HTTP_REFERER'))

