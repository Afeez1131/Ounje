from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not User.objects.filter(username=os.environ.get('USERNAME')).exists():
            User.objects.create_superuser(
                username=os.environ.get('USERNAME'),
                password=os.environ.get('PASSWORD')
            )
        print('Superuser has been created.')
