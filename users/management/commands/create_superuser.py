from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv()

username = os.getenv('ADMIN_USERNAME')
email = os.getenv('EMAIL_HOST_USER')
password = os.getenv('ADMIN_PASSWORD')
class Command(BaseCommand):
    help = 'Create a superuser with predefined credentials'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
