from carillon.models import Striker
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Check all strikers if they should be run in the current minute and run them if appropriate."

    def handle(self, *args, **options):
        Striker.run_checks()
        self.stdout.write(self.style.SUCCESS("Successfully checked and ran strikers."))
