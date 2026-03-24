from django.core.management.base import BaseCommand
from core.models import User

class Command(BaseCommand):
    help = 'Creates test users for each role'

    def handle(self, *args, **kwargs):
        users = [
            ('student1', 'student'),
            ('admin1', 'admin'),
            ('it1', 'it'),
        ]
        
        for username, role in users:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, password='password123', role=role)
                self.stdout.write(self.style.SUCCESS(f'Created user: {username} ({role})'))
            else:
                self.stdout.write(self.style.WARNING(f'User {username} already exists'))
