from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.TextField()
    response = models.TextField()