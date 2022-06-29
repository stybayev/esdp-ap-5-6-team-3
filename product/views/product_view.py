from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, \
    DetailView, DeleteView, FormView
from product.helpers import SearchView
from product.forms import ProductForm, SearchForm
from django.urls import reverse
from product.models import Product, Category
from googletrans import Translator
from transliterate import get_translit_function


translator = Translator()


class ProductDetailView(DetailView):
    context_object_name = 'product'
    template_name = 'product/detail_product_view.html'
    model = Product


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product

    def get_success_url(self):
        category = get_object_or_404(
            Category, pk=self.get_object().category_id)
        return reverse(
            'list_category_product',
            kwargs={'category': category.category_name})


class ProductCategoryListView(SearchView):
    template_name = 'product/list_product_view.html'
    model = Product
    ordering = ("created_at",)
    context_object_name = 'products'
    paginate_by = 15
    paginate_orphans = 1
    search_form = SearchForm
    search_fields = {
        'product_name': 'icontains',
        'description': 'icontains',
        'category__category_name': 'icontains',
        'price': 'icontains',
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, category_name=self.kwargs.get('category'))
        return context

    def get_queryset(self):
        return self.model.objects.filter(
            category__category_name__iexact=self.kwargs.get('category'))

    def get(self, request, *args, **kwargs):
        if request.GET.get('search') is None:
            return super().get(request, *args, **kwargs)
        search_param = request.GET.get('search')
        result = self.model.objects.filter(
            Q(product_name__icontains=search_param) |
            Q(description__icontains=search_param) |
            Q(category__category_name__icontains=search_param) |
            Q(price__icontains=search_param) |
            Q(translit_product_name__icontains=search_param) |
            Q(translit_description__icontains=search_param) |
            Q(product_name_translation__icontains=search_param) |
            Q(description_translation__icontains=search_param),
        )
        return render(request, self.template_name,
                      {self.context_object_name: result})


class ProductCreateView(LoginRequiredMixin, CreateView):
    template_name = 'product/create_product_view.html'
    form_class = ProductForm
    object = None

    def get_success_url(self):
        category = get_object_or_404(Category,
                                     pk=self.object.category_id)
        return reverse('list_category_product',
                       kwargs={'category': category.category_name})

    def cyrillic_check(self, text):
        lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        return lower.intersection(text.lower()) != set()

    def post(self, request, *args, **kwargs):
        translit_ru = get_translit_function('ru')
        form = self.form_class(data=request.POST, files=self.request.FILES)
        if form.is_valid():
            self.object = form.save(commit=False)
            product = self.object
            if self.cyrillic_check(product.product_name) is True:
                product.translit_product_name = translit_ru(
                    product.product_name, reversed=True)
                product.product_name_translation = translator.translate(
                    product.product_name, src='ru', dest='en').text
            elif self.cyrillic_check(product.product_name) is False:
                product.translit_product_name = translit_ru(
                    product.product_name)
                product.product_name_translation = translator.translate(
                    product.product_name, src='en', dest='ru').text
            if self.cyrillic_check(product.description) is True:
                product.translit_description = translit_ru(
                    product.description, reversed=True)
                product.description_translation = translator.translate(
                    product.description, src='ru', dest='en').text
            elif self.cyrillic_check(product.description) is False:
                product.translit_description = translit_ru(product.description)
                if product.description:
                    product.description_translation = translator.translate(
                        product.description, src='en', dest='ru').text
            product.save()
            return redirect(self.get_success_url())
        return render(request, self.template_name,
                      context={
                          'form': form
                      })


class ProductUpdateView(LoginRequiredMixin, FormView):
    template_name = 'product/update_product_view.html'
    form_class = ProductForm
    model = Product

    def cyrillic_check(self, text):
        lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        return lower.intersection(text.lower()) != set()

    def dispatch(self, request, *args, **kwargs):
        self.product = self.get_object()
        return super(ProductUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['product'] = self.product
        return super(ProductUpdateView, self).get_context_data(**kwargs)

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))

    def get_initial(self):
        initial = {}
        for key in 'product_name', 'category', 'photo', \
                   'description', 'available', 'price':
            initial[key] = getattr(self.product, key)
        return initial

    def form_valid(self, form):
        translit_ru = get_translit_function('ru')
        for key, value in form.cleaned_data.items():
            if value is not None:
                setattr(self.product, key, value)
        if self.cyrillic_check(self.product.product_name) is True:
            self.product.translit_product_name = translit_ru(
                self.product.product_name, reversed=True)
            self.product.product_name_translation = translator.translate(
                self.product.product_name, src='ru', dest='en').text
        elif self.cyrillic_check(self.product.product_name) is False:
            self.product.translit_product_name = translit_ru(
                self.product.product_name)
            self.product.product_name_translation = translator.translate(
                self.product.product_name, src='en', dest='ru').text
        if self.cyrillic_check(self.product.description) is True:
            self.product.translit_description = translit_ru(
                self.product.description, reversed=True)
            self.product.description_translation = translator.translate(
                self.product.description, src='ru', dest='en').text
        elif self.cyrillic_check(self.product.description) is False:
            self.product.translit_description = translit_ru(
                self.product.description)
            if self.product.description:
                self.product.description_translation = translator.translate(
                    self.product.description, src='en', dest='ru').text
        self.product.save()
        return super(ProductUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('detail_product', kwargs={'pk': self.get_object().pk})
