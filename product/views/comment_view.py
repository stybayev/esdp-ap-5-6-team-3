import telebot
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView

from config import client_key
from product.forms import CommentForm, SearchForm
from product.helpers import SearchView
from product.models import CustomerFeedback, Comments

bot = telebot.TeleBot(client_key)


class CommentListView(SearchView):
    template_name = 'comment/list_comment_view.html'
    model = Comments
    ordering = ("-id",)
    paginate_by = 10
    paginate_orphans = 1
    context_object_name = 'comments'
    search_form = SearchForm
    search_fields = {
        'feedback': 'icontains',
        'text': 'icontains',
    }


class CommentCreateView(CreateView):
    template_name = 'feedback/list_feedback_view.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        product_pk = kwargs.get('pk')
        product = get_object_or_404(CustomerFeedback, pk=product_pk)
        form = self.form_class(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.feedback_id = product.pk
            comment.save()
            print(comment.text)
            print(product.telegram_user_id_id)
            if product.description is not None:
                bot.send_message(
                    product.telegram_user_id_id,
                    f"_Оценка:{product.quiz_answer}, "
                    f"{product.description}_ \n\n"
                    f"*{comment.text}* \n ",
                    parse_mode='Markdown')
            else:
                bot.send_message(
                    product.telegram_user_id_id,
                    f"_Оценка:{product.quiz_answer}, без отзыва_ \n\n"
                    f"*{comment.text}* \n ",
                    parse_mode='Markdown')
            return redirect(
                reverse('detail_feedback', kwargs={'pk': product.pk}))
        return render(
            request,
            self.template_name,
            context={
                 'form': form
            }
        )
