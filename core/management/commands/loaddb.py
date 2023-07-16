import json

from django.core.management import BaseCommand

from core.models import Food


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('food.json', 'r') as file:
            content = json.load(file)

        for obj in content:
            name = obj.get('name')
            description = obj.get('description')
            category = obj.get('category')
            if not Food.objects.filter(name=name, description=description, category=category).exists():
                print('does not exist in DB')
                Food.objects.filter(name=name, description=description, category=category)
    print('Done loading foods from food.json into DB.')
