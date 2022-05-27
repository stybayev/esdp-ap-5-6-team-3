from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView
from product.helpers import SearchView
from product.forms import ProductForm, SearchForm
from django.urls import reverse, reverse_lazy
from product.models import Product, Review, Category
from accounts.models import Profile
from django.db.models import Avg
from django.db.models import Sum
from googletrans import Translator
from transliterate import translit, get_translit_function


translator = Translator()


def evaluate(request, pk):
    product_list = Product.objects.all()
    product = get_object_or_404(Product, id=request.POST.get('product_id'))
    evaluations = Review.objects.filter(product=product)
    product_avg_evaluation = evaluations.aggregate((Avg("evaluation")))
    print(product_avg_evaluation)
    return (product_avg_evaluation)


class ProductDetailView(DetailView):
    context_object_name = 'product'
    template_name = 'product/detail_product_view.html'
    model = Product

    # def get_context_data(self, **kwargs):
    #     kwargs['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
    #     product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
    #     evaluations = Review.objects.filter(product=product)
    #     product_avg_evaluation = evaluations.aggregate(Avg('evaluation'))
    #     context = {
    #         'product': product,
    #         'product_avg_evaluation': product_avg_evaluation
    #     }
    #     return context


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('list_product')


class MenuProductCategoryListView(SearchView):
    template_name = 'product/list_client_category_view.html'
    model = Category
    ordering = ("id",)
    context_object_name = 'categories'
    paginate_by = 5
    paginate_orphans = 1
    search_form = SearchForm
    search_fields = {
        'category_name': 'icontains',
        'translit_category_name': 'icontains',
        'category_name_translation': 'icontains'
    }


class ProductCategoryListView(SearchView):
    template_name = 'product/list_product_view.html'
    model = Product
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

    def get_queryset(self):
        return self.model.objects.filter(category__category_name__iexact=self.kwargs.get('category'))

    def get(self, request, *args, **kwargs):
        if request.GET.get('search') is None:
            return super().get(request, *args, **kwargs)
        search_param = request.GET.get('search')
        result = self.model.objects.filter(
            Q(product_name__icontains=search_param) | Q(description__icontains=search_param) |
            Q(category__category_name__icontains=search_param) | Q(price__icontains=search_param) |
            Q(translit_product_name__icontains=search_param) | Q(translit_description__icontains=search_param) |
            Q(product_name__icontains=translator.translate(search_param, src='ru', dest='en').text) |
            Q(product_name__icontains=translator.translate(search_param, src='en', dest='ru').text) |
            Q(description__icontains=translator.translate(search_param, src='ru', dest='en').text) |
            Q(description__icontains=translator.translate(search_param, src='en', dest='ru').text),
        )
        return render(request, self.template_name, {self.context_object_name: result})


class ProductCreateView(CreateView):
    template_name = 'product/create_product_view.html'
    form_class = ProductForm
    redirect_url = 'list_product'

    def cyrillic_check(self, text):
        lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        return lower.intersection(text.lower()) != set()

    def post(self, request, *args, **kwargs):
        translit_ru = get_translit_function('ru')
        form = self.form_class(data=request.POST, files=self.request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            if self.cyrillic_check(product.product_name) == True:
                product.translit_product_name = translit_ru(product.product_name, reversed=True)
                # product.translit_product_name = translit(product.product_name, language_code='ru', reversed=True)
            elif self.cyrillic_check(product.product_name) == False:
                product.translit_product_name = translit_ru(product.product_name)
                # product.translit_product_name = translit(product.product_name, 'ru')
            if self.cyrillic_check(product.description) == True:
                product.translit_description = translit_ru(product.description, reversed=True)
                # product.translit_description = translit(product.description, language_code='ru', reversed=True)
            elif self.cyrillic_check(product.description) == False:
                product.translit_description = translit_ru(product.description)
                # product.translit_description = translit(product.description, 'ru')
            # product.author = request.user
            product.save()
            return redirect(self.redirect_url)
        return render(request, self.template_name,
                      context={
                          'form': form
                      })


class ProductUpdateView(UpdateView):
    template_name = 'product/update_product_view.html'
    form_class = ProductForm
    model = Product

    def get_success_url(self):
        return reverse('detail_product', kwargs={'pk': self.get_object().pk})
