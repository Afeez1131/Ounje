from django.core.management import BaseCommand

from core.models import Food


class Command(BaseCommand):
    def handle(self, *args, **options):
        for food in Food.objects.all():
            try:
                print('food >> ', food.name)
                food = Food.objects.get(id=food.id)
                name = food.name
                split_name = name.split('.')
                digit = int(split_name[0])
                f_name = split_name[1]
                print(split_name, digit, f_name)
                print('setting name >>> from {} to {}'.format(name, f_name))
                food.name = f_name
                food.save()
                print('new name is : ', food.name)
            except:
                continue
