from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView, \
    UpdateView, DetailView, DeleteView
from product.forms import AboutusForm
from django.urls import reverse
from product.models import Aboutus
from product.services import aboutus_create


class AboutusView(ListView):
    """
        View для просмотра списка записей 'О нас'
    """
    context_object_name = 'aboutus'
    template_name = 'aboutus/aboutus_view.html'
    model = Aboutus


class AboutusDetailView(DetailView):
    """
        View для просмотра детального просмотра записи 'О нас'
    """
    context_object_name = 'aboutus'
    template_name = 'aboutus/detail_aboutus_view.html'
    model = Aboutus


class AboutUsDeleteView(LoginRequiredMixin, DeleteView):
    """
        View для удаления записи 'О нас'
    """
    template_name = 'aboutus/detail_aboutus_view.html'
    model = Aboutus

    def get(self, request, *args, **kwargs):
        return self.delete(request=request)

    def get_success_url(self):
        return reverse('aboutus_view')


class AboutusCreateView(LoginRequiredMixin, CreateView):
    """
        View для создания записи 'О нас'
    """
    template_name = 'aboutus/create_aboutus_view.html'
    form_class = AboutusForm
    object = None

    def get_success_url(self):
        return reverse('detail_aboutus', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            self.object = aboutus_create(request.POST)
            return redirect(self.get_success_url())
        return render(request, self.template_name,
                      context={
                          'form': form
                      })


class AboutusUpdateView(LoginRequiredMixin, UpdateView):
    """
        View для изменения записи 'О нас'
    """
    template_name = 'aboutus/update_aboutus_view.html'
    form_class = AboutusForm
    model = Aboutus

    def get_success_url(self):
        return reverse('detail_aboutus', kwargs={'pk': self.get_object().pk})
