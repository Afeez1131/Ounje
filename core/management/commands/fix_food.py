import random

from django.core.management import BaseCommand
from django.db.models import Count

from core.models import Food

swallow = ['Amala', 'Eba', 'Pounded Yam', 'Fufu', 'Àmàlà', 'Iyan']
soups = ['Efo riro', 'Egusi', 'Abula', 'Ila Asepo', 'Ogbono Soup', 'Obe Ata', 'Ọgbọnọ', 'Ọbẹ',
         'Bitter Leaf Soup', 'Ila-Asepo', 'Egusi Soup', 'Ewedu Soup', 'Gbegiri', 'Efo Gure',
         'Efo Egusi', 'Bitter Leaf', 'Obe Ata', 'Banga soup', 'Okro soup', 'Ogbono', 'Oha Soup'
         'Gbegiri Soup', 'Bitterleaf Soup', 'Obe ata dindin', 'Ofada Stew', 'Efo riro', 'Obe ila']


class Command(BaseCommand):
    def handle(self, *args, **options):
        for food in Food.objects.all():
            if food.name == 'Obe Ewedu':
                food.name = '{} and {}'.format(random.choice(swallow), food.name)
                food.save()
                print(food.name)
        # for soup in soups:
        #     if Food.objects.filter(name__iexact=soup).exists():
        #         sp = Food.objects.filter(name__iexact=soup)
        #         for s in sp:
        #             s_name = s.name
        #             print('soup >>> ', s_name)
        #             s.name = '{} and {}'.format(random.choice(swallow), s_name)
        #             s.save()
        #             print('after adding swallow: ', s.name)
        #
        # for swal in swallow:
        #     if Food.objects.filter(name__iexact=swal).exists():
        #         sw = Food.objects.filter(name__iexact=swal)
        #         for s in sw:
        #             print('swallow >>> ', s.name)
        #             s.name = '{} and {}'.format(s.name, random.choice(soups))
        #             s.save()
        #             print('after adding soup: ', s.name)
        # print('-----------------done-----------------')
