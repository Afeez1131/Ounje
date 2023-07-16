import csv
import json
import os
import random

import requests
from decouple import config
from django.http import JsonResponse, HttpResponse
from django_xhtml2pdf.utils import generate_pdf

from .enums import FoodCategoryChoices
from .models import Food

CATEGORY_CHOICE = FoodCategoryChoices.BREAKFAST
prompt2 = f''' Generate 20 list of Nigerian Yoruba dishes that are suitable for {CATEGORY_CHOICE} using the format given below.
name || description
To complete this task, follow these steps.
- should not be numbered.
- Research and compile list of 20 Nigerian Yoruba dishes, ensuring a diverse and wide range of options.
- ensure to put the correct Yoruba language mark on the name of each food.
- Review the structure and format of the generated data to ensure it meets the required output.
'''


def send_api_request(category):
    OPEN_API_KEY = config('OPEN_API_KEY')
    url = "https://api.openai.com/v1/completions"
    headers = {
        'Content-Type': 'Application/json',
        'Authorization': 'Bearer {}'.format(OPEN_API_KEY)
    }
    data = {
        'model': 'text-davinci-003',
        'prompt': prompt2,
        'temperature': 0.7,
        'max_tokens': 1050,
        'frequency_penalty': 0,
        'presence_penalty': 0
    }
    response = requests.post(url, json=data, headers=headers)
    try:
        formatted = response.json().get('choices')[0].get('text').split('\n')[1:]
        for item in formatted:
            name, description = item.split('||')
            Food.objects.create(name=name, description=description, category=category)
    except Exception as e:
        print(str(e))
        send_api_request(CATEGORY_CHOICE)


def write_pdf(template_src, context_dict):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachement; filename=food-table.pdf'
    result = generate_pdf(template_src, file_object=response, context=context_dict)
    return result


def get_download_type(request, food_list, filetype):
    if filetype == 'pdf':
        return generate_pdf_output(request, food_list)
    else:
        return generate_csv(request, food_list)


def generate_pdf_output(request, food_list):
    template = 'core/food_table.html'
    return write_pdf(template, {'food_list': food_list})


def generate_csv(request, food_list: list):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachement; filename="filename"'}
    )
    writer = csv.writer(response)
    writer.writerow(['Day', 'Breakfast', 'Lunch', 'Dinner'])
    for food_obj in food_list:
        day = food_obj.get('day')
        breakfast = food_obj.get('breakfast')
        lunch = food_obj.get('lunch')
        dinner = food_obj.get('dinner')
        writer.writerow([day, breakfast, lunch, dinner])
    return response
