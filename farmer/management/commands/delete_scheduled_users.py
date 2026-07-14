from django.core.management.base import BaseCommand
from django.utils import timezone
from farmer.models import User

class Command(BaseCommand):
    help = 'Deletes users who have passed their scheduled deletion date'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        users_to_delete = User.objects.filter(
            scheduled_deletion_date__isnull=False,
            scheduled_deletion_date__lte=now
        )
        
        count = users_to_delete.count()
        if count > 0:
            for user in users_to_delete:
                self.stdout.write(self.style.WARNING(f'Deleting user {user.email or user.contact}...'))
                user.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} user(s).'))
        else:
            self.stdout.write(self.style.SUCCESS('No users scheduled for deletion at this time.'))
