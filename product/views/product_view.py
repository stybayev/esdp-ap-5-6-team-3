from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from product.helpers import SearchView
from product.forms import ProductForm, SearchForm
from django.urls import reverse, reverse_lazy

from django.views.generic import RedirectView

from product.models import Product, Review
from accounts.models import Profile
from django.db.models import Avg
from django.db.models import Sum


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


class ProductListView(SearchView):
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


class ProductCreateView(CreateView):
    template_name = 'product/create_product_view.html'
    form_class = ProductForm
    redirect_url = 'list_product'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=self.request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
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
