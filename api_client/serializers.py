from rest_framework import serializers
from product.models import Basket, Product, Category, Comments


class BasketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basket
        fields = ['id', 'product', 'telegram_user_id',
                  'amount', 'product_total_price', 'status']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="category_name", read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'category', 'photo',
                  'description', 'price', 'available']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'translit_category_name',
                  'category_name_translation']
        read_only_fields = ['id']


class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ['id', 'feedback', 'text']
        read_only_fields = ['id']
