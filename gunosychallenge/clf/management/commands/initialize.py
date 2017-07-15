from django.core.management.base import BaseCommand
from .connect import Connect


class Command(BaseCommand):
    help = "initialize database"
    
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Initializing..."))
        self.initialize_database()
        self.stdout.write(self.style.SUCCESS("Successfully Initialized"))
        
        
    def initialize_database(self):
        con = Connect()
        con.delete_data()
        con.close()