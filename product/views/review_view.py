from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from ..helpers import DeleteView
from product.forms import ReviewForm
from product.models import Review, Product
from django.contrib.auth.mixins import PermissionRequiredMixin


class ProductReviewCreateView(CreateView):
    model = Review

    form_class = ReviewForm
    template_name = 'product/detail_product_view.html'

    def get_success_url(self):
        return reverse('detail_product',
                       kwargs={'pk': self.kwargs.get('pk')})

    def post(self, request, *args, **kwargs):
        product_pk = kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_pk)
        form = self.form_class(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.author = self.request.user
            review.save()
            return redirect(self.get_success_url())
        return render(request, self.template_name,
                      context={
                          'product': product,
                          'form': form
                      })


class ProductReviewUpdateView(PermissionRequiredMixin, UpdateView):
    model = Review
    template_name = 'review/product_review_update.html'
    context_object_name = 'review'
    form_class = ReviewForm
    permission_required = 'product.change_review'

    def has_permission(self):
        return (self.get_object().author == self.request.user or
                self.request.user.has_perm(self.permission_required))

    def get_success_url(self):
        return reverse('detail_product', kwargs={'pk': self.object.product.pk})


class ProductReviewDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'review/product_review_delete.html'
    model = Review
    confirm_deletion = True
    context_object_name = 'review'
    permission_required = 'product.delete_review'

    def test_func(self):
        return self.get_object().author == self.request.user or \
               self.request.user.has_perm(
            self.permission_required)

    def get_success_url(self):
        return reverse('detail_product', kwargs={'pk': self.object.product.pk})
