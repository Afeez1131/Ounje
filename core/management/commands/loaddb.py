import json

from django.core.management import BaseCommand

from core.models import Food


class Command(BaseCommand):
    def handle(self, *args, **options):
        Food.objects.all().delete()
        count = 0
        with open('food.json', 'r') as file:
            content = json.load(file)

        for obj in content:
            name = obj.get('name')
            description = obj.get('description')
            category = obj.get('category')
            if not Food.objects.filter(name=name, description=description, category=category).exists():
                count += 1
                print('creating {} '.format(name))
                Food.objects.create(name=name, description=description, category=category)
        print('Successfully Loaded {} Food into the DB'.format(count))
