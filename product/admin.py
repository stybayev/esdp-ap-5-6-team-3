from django.contrib import admin

# Register your models here.
from product.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'photo', 'text', 'created_at')
    list_filter = ['title']
    search_fields = ['text', 'title']
    fields = ['title', 'text', 'created_at', 'photo']
    readonly_fields = ['created_at']


admin.site.register(Product, ProductAdmin)
