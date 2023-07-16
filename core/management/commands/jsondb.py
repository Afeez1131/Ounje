import json

from django.core.management import BaseCommand

from core.models import Food

foods = []


class Command(BaseCommand):
    def handle(self, *args, **options):
        for food in Food.objects.all():
            d = {
                'name': food.name,
                'description': food.description,
                'category': food.category
            }
            foods.append(d)

        with open('food.json', 'w') as file:
            json.dump(foods, file)
    print('done writing DB to json')
