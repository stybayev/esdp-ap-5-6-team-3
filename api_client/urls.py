from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token


from api_client.views import ProductAPIView, BasketAPIView, CategoryAPIView

urlpatterns = [
    path('menu/', ProductAPIView.as_view(), name='menu_product'),
    path('basket/', BasketAPIView.as_view(), name='basket_client'),
    path('category/', CategoryAPIView.as_view(), name='category_client'),
]
