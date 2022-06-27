from django import forms

from product.models import (Product, Category,
                            Aboutus, ShoppingCartOrder, 
                            Comments, TableReservation)


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('product_name', 'category', 'photo',
                  'description', 'available', 'price')


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('category_name', )


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)


class AboutusForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Aboutus
        fields = ('description', 'telephone_number')


class ChangeOrderStatusForm(forms.ModelForm):
    class Meta:
        model = ShoppingCartOrder
        fields = ['status', ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text', )


class TableReservationForm(forms.ModelForm):
    class Meta:
        model = TableReservation
        fields = ['table_number', 'date', 'time', 'status']

