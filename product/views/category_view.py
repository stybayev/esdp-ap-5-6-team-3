from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from product.helpers import SearchView
from product.models import Category
from product.forms import CategoryForm, SearchForm


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
    }


class CategoryDetailView(DetailView):
    context_object_name = 'category'
    template_name = 'category/detail_category_view.html'
    model = Category


class CategoryCreateView(CreateView):
    template_name = 'category/create_category_view.html'
    form_class = CategoryForm
    redirect_url = 'list_category'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
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
