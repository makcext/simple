from django.core.management.base import BaseCommand, CommandError

# from django.conf import settings
from django.db import transaction


from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Populate development database with test data"

    def handle(self, *args, **options):
        sid = transaction.savepoint()
        try:
            with transaction.atomic():
                self.populate_db()
        except Exception as ex:
            transaction.rollback(sid)
            raise CommandError(f"\n{ex}\nRollback Database.", returncode=1)
        except KeyboardInterrupt:
            transaction.rollback(sid)
            print("interrupt")
            return

        self.success_print()

    def populate_db(self):

        # Create superuser
        User = get_user_model()
        if not User.objects.filter(username="simple").exists():
            User.objects.create_superuser(
                "simple",
                "chkr@simple.local",
                "simple",
            )
        self.stdout.write("Created superuser")

    def success_print(self):
        print("COMPLETED:")
        print("\t* Admin. login: simple, pass: simple, smpl@simple.local")
