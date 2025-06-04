from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Quiz.models import UserProfile

class Command(BaseCommand):
    help = 'Sets the admin flag for a user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to set as admin')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        try:
            user = User.objects.get(username=username)
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.is_admin = True
            profile.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully set admin flag for user {username}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} does not exist')) 