from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api_client.serializers import ProductSerializer, \
    BasketSerializer, CategorySerializer, CommentsSerializer
from product.models import Product, Basket, Category, Comments


class ProductAPIView(APIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(data=serializer.data)


class CategoryAPIView(APIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
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


# @csrf_exempt
class CommentsAPIView(APIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    # permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset.all(), many=True)
        print(serializer)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
