from django.urls import path

from core import views
from core.views import generate_food, generate_random_food, generate_output

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('generate-food', generate_food, name='generate_food'),
    path('ajax-food', generate_random_food, name='get_random_food'),
    path('generate-output', generate_output, name='generate_output'),
]
