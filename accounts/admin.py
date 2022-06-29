from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from product.models import MerchantTelegramUser


# Register your models here.


class ProfileInline(admin.StackedInline):
    model = MerchantTelegramUser
    fields = ['user_id', 'first_name', 'last_name', 'phone_number', 'vcard']


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline, ]


User = get_user_model()
admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)
