from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api_client.serializers import ProductSerializer, BasketSerializer
from product.models import Product, Basket


class ProductAPIView(APIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(data=serializer.data)


class BasketAPIView(APIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    model = Basket
    # permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(data=serializer.data)

    # def post(self, request, *args, **kwargs):
    #     product_pk = kwargs['pk']
    #     basket = get_object_or_404(Product, pk=product_pk)
    #     if not self.model.objects.filter(post_id=product_pk, author_id=self.request.user.pk):
    #         self.model.objects.create(post_id=product_pk, author_id=self.request.user.pk)
    #         basket.like_count += 1
    #         basket.save()
    #     else:
    #         basket.like_count -= 1
    #         basket.save()
    #         self.model.objects.filter(post_id=product_pk, author_id=self.request.user.pk).delete()
    #
    #     data = {'likes_count': basket.like_count}
    #     return JsonResponse(data)
