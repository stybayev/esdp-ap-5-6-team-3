from django.contrib.auth import authenticate, login, logout, \
    get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView, UpdateView
from accounts.forms import (UserCreationForm, UserChangeForm,
                            ProfileChangeForm, PasswordChangeForm)
from django.views import View
from product.models import MerchantTelegramUser


class LoginView(View):
    """
        View для аутентификации пользователя
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/login.html', context={
            'next': request.GET.get('next')
        })

    def post(self, request, *args, **kwargs):
        context = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        next_page = request.GET.get('next')
        if user is not None:
            login(request, user)
            if next_page is not None:
                return redirect(next_page)
            return redirect('/')
        else:
            context['has_error'] = True
        return render(request, 'registration/login.html', context=context)


class LogoutView(View):
    """
        View для выхода пользователя из авторизации CRM проекта
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('list_category')


def register(request, m):
    """
        Регистрация пользователя через телеграм бот мерчанта,
        а такше создание профиля пользователя
    """
    user_form = UserCreationForm({'username': f'{m.contact.user_id}',
                                  'first_name': f'{m.contact.first_name}',
                                  'last_name': f'{m.contact.last_name}',
                                  'password': f'{m.contact.phone_number[1:]}',
                                  'password_confirm':
                                      f'{m.contact.phone_number[1:]}',
                                  'email': ''})
    print(m.contact.phone_number[1:])
    if user_form.is_valid():
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        MerchantTelegramUser.objects.get_or_create(
            user_id=m.contact.user_id, first_name=m.contact.first_name,
            last_name=m.contact.last_name, phone_number=m.contact.phone_number,
            vcard=m.contact.vcard, auth_user_id=new_user.pk)


class UserProfileView(DetailView):
    """
        Просмотр профиля пользователя
    """
    model = get_user_model()
    template_name = 'profile/profile.html'
    context_object_name = 'user_obj'


class UserProfileUpdateView(UpdateView):
    """
        Редактирование профиля пользователя
    """
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'profile/user_profile_update.html'
    context_object_name = 'user_obj'

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.auth_user_profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        first_name = self.request.POST.get('first_name')
        last_name = self.request.POST.get('last_name')
        for merchant in MerchantTelegramUser.objects.all():
            if merchant.auth_user == self.request.user:
                merchant.first_name = first_name
                merchant.last_name = last_name
                merchant.save()
        return response

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})


class ChangePasswordView(LoginRequiredMixin, UpdateView):
    """
        Изменение пароля пользователя через профиль пользователя в CRM проекте
    """
    model = get_user_model()
    template_name = 'registration/change_password.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.user.id)


def change_password(request, m):
    """
        Сброс/Изменение пароля через телеграм бот мерчанта
    """
    for merchant in MerchantTelegramUser.objects.all():
        if merchant.user_id == m.from_user.id:
            user = merchant.auth_user
            user.set_password(f'{merchant.phone_number}')
            user.save()
