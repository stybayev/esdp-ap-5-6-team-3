from rest_framework import serializers
from product.models import Basket, Product
from django.contrib.auth import get_user_model


# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         read_only_fields = ['id']
#         exclude = ['password', 'groups', 'user_permissions']


class BasketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basket
        fields = ['id', 'product', 'telegram_user_id', 'amount', 'product_total_price', 'status']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'category', 'photo', 'description', 'price', 'available']
        read_only_fields = ['id']

