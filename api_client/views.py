import telebot
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api_client.serializers import ProductSerializer, \
    BasketSerializer, CategorySerializer, CommentsSerializer
from config import client_key
from product.models import Product, Basket, Category, Comments, CustomerFeedback

bot = telebot.TeleBot(client_key)


class ProductAPIView(APIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(data=serializer.data)


class CategoryAPIView(APIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(data=serializer.data)


class BasketAPIView(APIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    model = Basket

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(data=serializer.data)


class CommentsAPIView(APIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    # permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        for feedback in CustomerFeedback.objects.all():
            if feedback.id == int(self.request.data['feedback']):
                if feedback.description is not None:
                    bot.send_message(feedback.telegram_user_id_id,
                                     f"_Оценка:{feedback.quiz_answer}, {feedback.description}_ \n\n"
                                     f"*{self.request.data['text']}* \n ",
                                     parse_mode='Markdown')
                else:
                    bot.send_message(feedback.telegram_user_id_id,
                                     f"_Оценка:{feedback.quiz_answer}, без отзыва_ \n\n"
                                     f"*{self.request.data['text']}* \n ",
                                     parse_mode='Markdown')
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
