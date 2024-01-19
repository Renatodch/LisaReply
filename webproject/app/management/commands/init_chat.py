from app.chat import Chatbot
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Initialize the Django project'

    def handle(self, *args, **options):
        Chatbot.get_instance()
        pass