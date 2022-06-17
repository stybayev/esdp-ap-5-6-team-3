from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator


class CoolModelBro(Model):
    limited_integer_field = IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
     )