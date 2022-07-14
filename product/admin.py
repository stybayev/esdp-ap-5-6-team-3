from django.contrib import admin
from product.models import (Product, Category, StatusShoppingCartOrder,
                            TelegramUser, MerchantTelegramUser)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'photo', 'description',
                    'created_at', 'price', 'available', 'category')
    list_filter = ['product_name']
    search_fields = ['product_name', 'category']
    fields = ['product_name', 'photo', 'description',
              'price', 'available', 'category']
    readonly_fields = ['created_at']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    list_filter = ['category_name']
    search_fields = ['category_name']
    fields = ['category_name']
    readonly_fields = ['id']


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'status']
    search_fields = ['status']
    fields = ['status']


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name',
                    'phone_number', 'vcard')
    list_filter = ['first_name']
    search_fields = ['first_name', 'last_name', 'phone_number']
    fields = ['first_name']
    readonly_fields = ['user_id']


class MerchantTelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name',
                    'phone_number', 'vcard')
    list_filter = ['first_name']
    search_fields = ['first_name', 'last_name', 'phone_number']
    fields = ['first_name']
    readonly_fields = ['user_id']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(StatusShoppingCartOrder, StatusAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(MerchantTelegramUser, MerchantTelegramUserAdmin)
