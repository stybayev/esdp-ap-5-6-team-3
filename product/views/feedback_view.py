from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import DetailView

from product.forms import SearchForm
from product.helpers import SearchView
from product.models import CustomerFeedback
from django.db.models import Sum, Avg


class CustomerFeedbackListView(SearchView):
    """
        View для просмотра списка записей 'Отзывов'
    """
    template_name = 'feedback/list_feedback_view.html'
    model = CustomerFeedback
    ordering = ("-id",)
    paginate_by = 10
    paginate_orphans = 1
    context_object_name = 'feedbacks'
    search_form = SearchForm
    search_fields = {
        'quiz_answer': 'icontains',
        'description': 'icontains',
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        feedback = self.model.objects.all()
        if feedback.exists():
            sum_quiz_answer = self.model.objects.aggregate(Sum('quiz_answer'))
            avg_quiz_answer = self.model.objects.aggregate(Avg('quiz_answer'))
            kwargs['sum_quiz_answer'] = sum_quiz_answer['quiz_answer__sum']
            kwargs['avg_quiz_answer'] = round(
                avg_quiz_answer['quiz_answer__avg'], 2)
            kwargs['round_avg_quiz_answer'] = round(
                avg_quiz_answer['quiz_answer__avg'])
            return super().get_context_data(**kwargs)


class CustomerFeedbackDetailView(LoginRequiredMixin, DetailView):
    """
        View для детального просмотра записи 'Отзыва'
    """
    context_object_name = 'feedback'
    template_name = 'feedback/detail_feedback_view.html'
    model = CustomerFeedback
    paginate_related_by = 5
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        comments = self.object.feedback_comments.order_by('-id')
        paginator = Paginator(comments, self.paginate_related_by,
                              orphans=self.paginate_related_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['comments'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)
