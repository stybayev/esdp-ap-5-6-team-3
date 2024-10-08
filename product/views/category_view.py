from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView
from product.helpers import SearchView
from product.models import Category
from product.forms import CategoryForm, SearchForm
from transliterate import translit
from googletrans import Translator

from product.services import category_create

translator = Translator()


class CategoryListView(SearchView):
    """
        View для просмотра списка всех записей по 'Категориям' продуктов
    """
    template_name = 'category/list_category_view.html'
    model = Category
    ordering = ("id",)
    context_object_name = 'categories'
    search_form = SearchForm
    search_fields = {
        'category_name': 'icontains',
        'translit_category_name': 'icontains',
        'category_name_translation': 'icontains'
    }


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """
        View для создания записи 'Категории' продукта
    """
    template_name = 'category/create_category_view.html'
    form_class = CategoryForm
    redirect_url = 'list_category'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            category_create(request.POST)
            return redirect(self.redirect_url)
        return render(request, self.template_name,
                      context={
                          'form': form
                      })


class CategoryUpdateView(LoginRequiredMixin, FormView):
    """
        View для изменения записи 'Категории' продукта
    """
    template_name = 'category/update_category_view.html'
    form_class = CategoryForm
    model = Category
    success_url = 'list_category'

    def cyrillic_check(self, text):
        lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        return lower.intersection(text.lower()) != set()

    def dispatch(self, request, *args, **kwargs):
        self.category = self.get_object()
        print(super(
            CategoryUpdateView, self).dispatch(request, *args, **kwargs))
        return super(
            CategoryUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['category'] = self.category
        return super(CategoryUpdateView, self).get_context_data(**kwargs)

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))

    def get_initial(self):
        initial = {}
        for key in 'category_name', :
            initial[key] = getattr(self.category, key)
        return initial

    def form_valid(self, form):
        for key, value in form.cleaned_data.items():
            if value is not None:
                setattr(self.category, key, value)
        if self.cyrillic_check(self.category.category_name) is True:
            self.category.translit_category_name = translit(
                self.category.category_name, language_code='ru', reversed=True)
            self.category.category_name_translation = translator.translate(
                self.category.category_name, src='ru', dest='en').text
        else:
            self.category.translit_category_name = translit(
                self.category.category_name, 'ru')
            self.category.category_name_translation = translator.translate(
                self.category.category_name, src='en', dest='ru').text
        self.category.save()
        return super(CategoryUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('list_category')


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    """
        View для удаления записи 'Категории' продукта
    """
    model = Category
    success_url = reverse_lazy('list_category')
