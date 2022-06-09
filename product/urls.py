from django.urls import path

from product.views.aboutus_view import AboutusCreateView, AboutusView, AboutusUpdateView, AboutusDetailView
from product.views.basket_view import BasketProductListView, AddBasketView, SubtractBasketView, BasketListView
from product.views.order_view import OrderListView
from product.views.review_view import ProductReviewCreateView, ProductReviewUpdateView, ProductReviewDeleteView

from product.views.product_view import (ProductCreateView, ProductDetailView, ProductDeleteView,
                                        evaluate, ProductUpdateView, ProductCategoryListView,
                                        MenuProductCategoryListView
                                        )
from product.views.category_view import (CategoryCreateView, CategoryListView, CategoryUpdateView,
                                         CategoryDeleteView, CategoryDetailView)

urlpatterns = []

product_urls = [
    path('product/add', ProductCreateView.as_view(), name='create_product'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='detail_product'),
    path('', MenuProductCategoryListView.as_view(), name='list_product'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='delete_product'),
    path('evaluate/<int:pk>', evaluate, name='evaluate'),
    path('product/<int:pk>/update', ProductUpdateView.as_view(), name='update_product'),
    path('product/<str:category>/', ProductCategoryListView.as_view(), name='list_category_product'),
]

review_urls = [
    path('product/<int:pk>/review', ProductReviewCreateView.as_view(), name='create_review'),
    path('product/review/<int:pk>/update', ProductReviewUpdateView.as_view(), name='update_review'),
    path('product/review/<int:pk>/delete', ProductReviewDeleteView.as_view(), name='delete_review')
]

category_urls = [
    path('category/add', CategoryCreateView.as_view(), name='create_category'),
    path('category', CategoryListView.as_view(), name='list_category'),
    path('category/<int:pk>/delete', CategoryDeleteView.as_view(), name='delete_category'),
    path('category/<int:pk>/update', CategoryUpdateView.as_view(), name='update_category'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='detail_category'),
]

basket_urls = [
    path('basket_menu', BasketProductListView.as_view(), name='list_basket'),
    path('basket_menu/<int:pk>/add/', AddBasketView.as_view(), name='add_basket'),
    path('basket_menu/<int:pk>/subtract/', SubtractBasketView.as_view(), name='subtract_basket'),
    path('basket', BasketListView.as_view(), name='basket_all'),
]

aboutus_urls = [
    path('aboutus/add', AboutusCreateView.as_view(), name='create_aboutus'),
    path('aboutus/', AboutusView.as_view(), name='aboutus_view'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='delete_product'),
    path('aboutus/<int:pk>/detail', AboutusDetailView.as_view(), name='detail_aboutus'),
    path('aboutus/<int:pk>/update', AboutusUpdateView.as_view(), name='update_aboutus')
]


orders_urls = [
    path('orders/', OrderListView.as_view(), name='orders_view'),
]

urlpatterns += product_urls
urlpatterns += review_urls
urlpatterns += category_urls
urlpatterns += basket_urls
urlpatterns += aboutus_urls
urlpatterns += orders_urls
