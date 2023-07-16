from django.urls import path

from api import views

urlpatterns = [
    path('random', views.RandomFood.as_view(), name='random_food'),
    path('foods', views.FoodList.as_view(), name='food_list'),
]
