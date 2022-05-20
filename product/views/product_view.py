from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView
from product.helpers import FormView as CustomFormView, SearchView, DetailView
from product.forms import ProductForm, SearchForm
from django.urls import reverse

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

    def get_context_data(self, **kwargs):
        kwargs['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        evaluations = Review.objects.filter(product=product)
        product_avg_evaluation = evaluations.aggregate(Avg('evaluation'))
        context = {
            'product': product,
            'product_avg_evaluation': product_avg_evaluation
        }
        return context


class DeleteView(RedirectView):
    pattern_name = 'list_product'

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        product.delete()
        return redirect(self.get_redirect_url())



class ProductListView( SearchView):
    template_name = 'product/list_product_view.html'
    model = Product
    ordering = ("created_at",)
    context_object_name = 'products'

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['form'] = self.form

        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(title__icontains=self.search_value) | Q(text__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

class ProductCreateView(LoginRequiredMixin, CustomFormView):
    template_name = 'product/create_product_view.html'
    form_class = ProductForm
    redirect_url = ''

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=self.request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            return redirect('list_product')
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


