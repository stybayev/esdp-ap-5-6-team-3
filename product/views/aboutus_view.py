from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from product.forms import ProductForm, SearchForm, AboutusForm
from django.urls import reverse

from django.views.generic import RedirectView

from product.models import Product, Review, Aboutus
from accounts.models import Profile
from django.db.models import Avg


class AboutusView(ListView):
    context_object_name = 'aboutus'
    template_name = 'aboutus/aboutus_view.html'
    model = Aboutus

class AboutusDetailView(DetailView):
    context_object_name = 'aboutus'
    template_name = 'aboutus/detail_aboutus_view.html'
    model = Aboutus

class DeleteView(RedirectView):
    pattern_name = 'list_product'

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        product.delete()
        return redirect(self.get_redirect_url())

class AboutusCreateView(LoginRequiredMixin, CreateView):
    template_name = 'aboutus/create_aboutus_view.html'
    form_class = AboutusForm
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


class AboutusUpdateView(UpdateView):
    template_name = 'aboutus/update_aboutus_view.html'
    form_class = AboutusForm
    model = Aboutus

    def get_success_url(self):
         return reverse('detail_aboutus', kwargs={'pk': self.get_object().pk})


