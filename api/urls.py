from django.urls import path

from api import views

urlpatterns = [
    path('random', views.RandomFood.as_view()),
    path('foods', views.FoodList.as_view()),
    # user creation
    path('register', views.CreateUserAccount.as_view()),
]
