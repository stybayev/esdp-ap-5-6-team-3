from typing import Dict

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from urllib.parse import urlencode

from django.views.generic import ListView, TemplateView


class SearchView(ListView):
    template_name = None
    model = None
    ordering = ('-created_at',)
    paginate_by = 5
    context_object_name = 'products'
    search_form = None
    search_fields: Dict[str, str] = {}

    def get_search_form(self):
        return self.search_form(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({
                'search': self.search_value
            })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q()
            query_list = [
                Q(**{f"{key}__{value}": self.search_value})
                for key, value in self.search_fields.items()
            ]
            for query_part in query_list:
                query = (query | query_part)
            query = Q(title__icontains=self.search_value) | Q(text__icontains=self.search_value)

            queryset = queryset.filter(query)
        return queryset


class FormView(View):
    form_class = None
    template_name = None
    redirect_url = ''
    model = None
    object = None

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context=context)

    def get_context_data(self, **kwargs):
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_redirect_url())

    def form_invalid(self, form):
        form.save()
        context = self.get_context_data(form=form)
        return render(self.request, self.template_name, context=context)

    def get_redirect_url(self):
        return self.redirect_url


class DetailView(TemplateView):
    context_object_name = 'object'
    model = None
    key_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.get_object()
        return context

    def get_object(self):
        pk = self.kwargs.get(self.key_kwarg)
        return get_object_or_404(self.model, pk=pk)


class DeleteView(View):
    template_name = None
    confirm_deletion = True
    model = None
    key_kwarg = 'pk'
    context_object_name = 'object'
    success_url = ''

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.confirm_deletion:
            return render(request, self.template_name, self.get_context_data())
        else:
            self.perform_delete()
            return redirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.perform_delete()
        return redirect(self.get_success_url())

    def perform_delete(self):
        self.object.delete()

    def get_context_data(self, **kwargs):
        return {
            self.context_object_name: self.object
        }

    def get_object(self):
        pk = self.kwargs.get(self.key_kwarg)
        return get_object_or_404(self.model, pk=pk)

    def get_success_url(self):
        return self.success_url
