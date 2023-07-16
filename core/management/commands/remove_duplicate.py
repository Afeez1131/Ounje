from django.core.management import BaseCommand
from django.db.models import Count

from core.models import Food


class Command(BaseCommand):
    def handle(self, *args, **options):
        duplicate_names = Food.objects.values('name').annotate(name_count=Count('name')).filter(name_count__gt=1)
        print('food with duplicate names greater than 1: ', duplicate_names)
        for name in duplicate_names:
            to_keep = Food.objects.filter(name=name['name']).first()
            Food.objects.filter(name=name['name']).exclude(id=to_keep.id).delete()
