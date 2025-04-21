# from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "DELETE ALL DATA FROM DEV DATABASE."

    def handle(self, *args, **options):
        # if settings.ENV == "production":
        #     print("Cannot clear DB in PRODUCTION environment")
        #     return

        management.call_command("flush", verbosity=0, interactive=False)
