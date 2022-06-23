from django.urls import path


from api_client.views import ProductAPIView, BasketAPIView, CategoryAPIView

urlpatterns = [
    path('menu/', ProductAPIView.as_view(), name='menu_product'),
    path('basket/', BasketAPIView.as_view(), name='basket_client'),
    path('category/', CategoryAPIView.as_view(), name='category_client'),
]
