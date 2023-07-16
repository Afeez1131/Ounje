from django.contrib.auth.models import User
from django.db import models

from core.enums import FoodCategoryChoices


# Create your models here.

class Food(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField()
    category = models.CharField(max_length=155, choices=FoodCategoryChoices.choices)

    def __str__(self):
        return '{}: {}'.format(self.name, self.category)


# Day 1, 2, 3...
## Category: Breakfast, Lunch

class DayFood(models.Model):
    day = models.PositiveIntegerField(default=1)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.user.username, self.food.name)

