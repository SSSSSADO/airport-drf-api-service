from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create demo superuser if it does not exist."

    def handle(self, *args, **options):
        User = get_user_model()
        email = "admin@example.com"
        password = "SuperPass777"

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f"Demo superuser {email} already exists.")
            )
            return
        
        User.objects.create_superuser(
            email=email,
            password=password,
            first_name="Demo",
            last_name="Admin",
        )

        self.stdout.write(
            self.style.SUCCESS(f"Created demo superuser: {email}")
        )
