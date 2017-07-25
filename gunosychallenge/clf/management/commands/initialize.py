from django.core.management.base import BaseCommand
from .connect import Connect


class Command(BaseCommand):
    """
    A command which initializes the database.

    Use this class if you want to delete all data and initialize the database.

    Several attributes affect behaviour.

    ``help``
        A short description of the command, which will be printed in
        help messages.
    """
    help = "Delete all data and Initialize database."

    def handle(self, *args, **options):
        """Handle a event in response to the argument 'initialize'."""
        self.stdout.write(self.style.SUCCESS("Initializing..."))
        self._initialize_database()
        self.stdout.write(self.style.SUCCESS("Successfully Initialized"))

    def _initialize_database(self):
        """Delete all data."""
        con = Connect()
        con.delete_data()
        con.close()
