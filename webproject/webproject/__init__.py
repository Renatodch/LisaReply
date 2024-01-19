from django import setup
setup()
from app.chat import Chatbot
Chatbot.get_instance()