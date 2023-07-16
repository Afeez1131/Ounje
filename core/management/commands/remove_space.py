from django.core.management import BaseCommand

from core.models import Food


class Command(BaseCommand):
    def handle(self, *args, **options):
        for food in Food.objects.all():
            print('before "{}"'.format(food.name))
            name = food.name.lstrip().rstrip()
            food.name = name
            food.save()
            print('after "{}"'.format(food.name))
