from django.core.management import call_command
from django.core.management.base import BaseCommand
from airport.models import Country


class Command(BaseCommand):
    help = "Load demo data if the database is empty."

    def handle(self, *args, **options):
        if Country.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Demo data already exists. Skipping fixture loading."
                )
            )
            return

        call_command("loaddata", "airport_data")
        self.stdout.write(
            self.style.SUCCESS(
                "Demo data successfully loaded."
            )
        )
