from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from product.helpers import SearchView
from product.models import Category
from product.forms import CategoryForm, SearchForm
from transliterate import translit
from googletrans import Translator


translator = Translator()


class CategoryListView(SearchView):
    template_name = 'category/list_category_view.html'
    model = Category
    ordering = ("id",)
    context_object_name = 'categories'
    paginate_by = 10
    paginate_orphans = 1
    search_form = SearchForm
    search_fields = {
        'category_name': 'icontains',
        'translit_category_name': 'icontains',
        'category_name_translation': 'icontains'
    }


class CategoryDetailView(DetailView):
    context_object_name = 'category'
    template_name = 'category/detail_category_view.html'
    model = Category


class CategoryCreateView(CreateView):
    template_name = 'category/create_category_view.html'
    form_class = CategoryForm
    redirect_url = 'list_category'

    def cyrillic_check(self, text):
        lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        return lower.intersection(text.lower()) != set()

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            if self.cyrillic_check(category.category_name) == True:
                category.translit_category_name = translit(category.category_name, language_code='ru', reversed=True)
                category.category_name_translation = translator.translate(category.category_name.lower(), src='ru', dest='en').text
            else:
                category.translit_category_name = translit(category.category_name, 'ru')
                category.category_name_translation = translator.translate(category.category_name.lower(), src='en', dest='ru').text
            category.save()
            return redirect(self.redirect_url)
        return render(request, self.template_name,
                      context={
                          'form': form
                      })


class CategoryUpdateView(UpdateView):
    template_name = 'category/update_category_view.html'
    form_class = CategoryForm
    model = Category
    success_url = 'list_category'

    def get_success_url(self):
        return reverse('list_category')


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('list_category')
