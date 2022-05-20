from django import forms

from product.models import Product, Review


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('title', 'category', 'photo', 'text', 'status', 'price')


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'evaluation']

