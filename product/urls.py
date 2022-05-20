from django.urls import path

from product.views.review_view import ProductReviewCreateView, ProductReviewUpdateView, ProductReviewDeleteView

from product.views.product_view import ProductCreateView, ProductDetailView, ProductListView, DeleteView, evaluate, \
    ProductUpdateView

urlpatterns = []

product_urls = [
    path('product/add', ProductCreateView.as_view(), name='create_product'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='detail_product'),
    path('', ProductListView.as_view(), name='list_product'),
    path('product/<int:pk>/delete', DeleteView.as_view(), name='delete_product'),
    path('evaluate/<int:pk>', evaluate, name='evaluate'),
    path('product/<int:pk>/update', ProductUpdateView.as_view(), name='update_product'),
]

review_urls = [
    path('product/<int:pk>/review', ProductReviewCreateView.as_view(), name='create_review'),
    path('product/review/<int:pk>/update', ProductReviewUpdateView.as_view(), name='update_review'),
    path('product/review/<int:pk>/delete', ProductReviewDeleteView.as_view(), name='delete_review')
]

urlpatterns += product_urls
urlpatterns += review_urls
