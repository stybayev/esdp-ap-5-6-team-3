from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
# from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    GENDER = [
        ('they', 'Не задано'),
        ('woman', 'Женщина'),
        ('man', 'Мужчина'),
    ]

    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    avatar = models.ImageField(null=False, blank=False, upload_to='user_pics', verbose_name='Аватар')
    about_profile = models.TextField(null=True, blank=True, max_length=1000, verbose_name='О себе')
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='Номер телефона')
    gender = models.CharField(null=True, blank=True, choices=GENDER, verbose_name='Пол', max_length=20)

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"
