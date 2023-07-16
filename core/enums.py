from django.db import models


class FoodCategoryChoices(models.TextChoices):
    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'
