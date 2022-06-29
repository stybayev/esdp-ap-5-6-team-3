from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView, \
    UpdateView, DetailView, DeleteView
from product.forms import AboutusForm
from django.urls import reverse
from product.models import Aboutus


class AboutusView(ListView):
    context_object_name = 'aboutus'
    template_name = 'aboutus/aboutus_view.html'
    model = Aboutus


class AboutusDetailView(DetailView):
    context_object_name = 'aboutus'
    template_name = 'aboutus/detail_aboutus_view.html'
    model = Aboutus


class AboutUsDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'aboutus/detail_aboutus_view.html'
    model = Aboutus

    def get(self, request, *args, **kwargs):
        return self.delete(request=request)

    def get_success_url(self):
        return reverse('aboutus_view')


class AboutusCreateView(LoginRequiredMixin, CreateView):
    template_name = 'aboutus/create_aboutus_view.html'
    form_class = AboutusForm
    object = None

    def get_success_url(self):
        return reverse('detail_aboutus', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            return redirect(self.get_success_url())
        return render(request, self.template_name,
                      context={
                          'form': form
                      })


class AboutusUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'aboutus/update_aboutus_view.html'
    form_class = AboutusForm
    model = Aboutus

    def get_success_url(self):
        return reverse('detail_aboutus', kwargs={'pk': self.get_object().pk})
