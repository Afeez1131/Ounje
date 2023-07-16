import csv
import json
import random

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from core.enums import FoodCategoryChoices
from core.models import Food
from core.utils import write_pdf, get_download_type


class HomePage(TemplateView):
    template_name = 'core/home.html'


def generate_food(request):
    try:
        count = int(request.GET.get('count'))
        foods = Food.objects.all()
        breakfast = foods.filter(category=FoodCategoryChoices.BREAKFAST)
        lunch = foods.filter(category=FoodCategoryChoices.LUNCH)
        dinner = foods.filter(category=FoodCategoryChoices.DINNER)

        lunch_list = list(lunch.values_list('name', flat=True))
        breakfast_list = list(breakfast.values_list('name', flat=True))
        dinner_list = list(dinner.values_list('name', flat=True))
        food_list = []
        for i in range(count):
            random.shuffle(breakfast_list)
            random.shuffle(lunch_list)
            random.shuffle(dinner_list)

            food_dict = dict()
            breakfast = random.choice(breakfast_list)
            lunch = random.choice(lunch_list)
            dinner = random.choice(dinner_list)

            food_dict['breakfast'] = breakfast
            food_dict['lunch'] = lunch
            food_dict['dinner'] = dinner

            food_list.append(food_dict)
        output = render_to_string('core/ajax_food.html', {'food_list': food_list})
        return JsonResponse({'status': 'success', 'output': output})
    except:
        return JsonResponse({'status': 'error'})


def generate_random_food(request):
    id = request.GET.get('id')
    foods = Food.objects.all()
    food_ids = foods.values_list('id', flat=True)
    random_food_id = random.choice(food_ids)
    food = Food.objects.get(id=random_food_id).name
    return JsonResponse({'food': food})


def generate_output(request):
    filetype = request.POST.get('file_type')
    output = request.POST.get('output')
    json_output = json.loads(output)[1:]
    return get_download_type(request, json_output, filetype)


