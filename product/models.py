from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.deletion import get_candidate_relations_to_delete
from imagekit.models import ImageSpecField
from pilkit.processors import Transpose, ResizeToFill


class CustomModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Entity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания", blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = CustomModelManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        delete_candidates = get_candidate_relations_to_delete(self.__class__._meta)
        if delete_candidates:
            for rel in delete_candidates:
                if rel.on_delete.__name__=='CASCADE' and rel.one_to_many and not rel.hidden:
                    for item in getattr(self, rel.related_name).all():
                        item.delete()
        self.save(update_fields=['is_deleted',])

    class Meta:
        abstract = True

class Category(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.title


class Product(Entity):
    STATUS = [
        ('Есть', 'есть'),
        ('Нет', 'нет'),
        ]
    title = models.CharField(max_length=100, null=False, blank=False)
    category = models.ForeignKey('product.Category', on_delete=models.CASCADE, null=False, blank=False, default=1)
    photo = models.ImageField(upload_to='products/photos',
                              verbose_name='Фото',
                              null=True,
                              blank=True)

    text = models.TextField(max_length=3000,
                            null=True,
                            blank=True)
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.SET_DEFAULT,
                               default=1,
                               related_name='products',
                               verbose_name='Автор'
                               )
    price = models.PositiveIntegerField(null=False, blank=False, default=0)
    status = models.CharField(null=False, blank=False, choices=STATUS, verbose_name='наличие', default="есть", max_length=20)


    def __str__(self):
        return f"{self.pk}. {self.title}"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        permissions = [
            ('can_use_it', 'Можно использовать это')
        ]


class Review(Entity):
    product = models.ForeignKey('product.Product',
                             related_name='reviews',
                             on_delete=models.CASCADE,
                             verbose_name='Продукт')
    text = models.TextField(max_length=400,
                            verbose_name='Отзыв', null=False, blank=False)
    author = models.ForeignKey(
                            get_user_model(),
                            on_delete=models.SET_DEFAULT,
                            related_name='reviews',
                            default=1,
                            verbose_name='Автор'
                            )
    evaluation = models.PositiveIntegerField(null=False, blank=False, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.text[:20]
