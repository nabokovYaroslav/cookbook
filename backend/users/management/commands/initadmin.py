import os

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).count() == 0:
            username = os.environ.get("SUPERUSER_USERNAME")
            email = os.environ.get("SUPERUSER_EMAIL")
            password = os.environ.get("SUPERUSER_PASSWORD")
            print('Creating account for %s (%s)' % (username, email))
            admin = User.objects.create_superuser(email=email, user_name=username, password=password)
            admin.save()
            print('Successfully created')
        else:
            print('Admin already exist')