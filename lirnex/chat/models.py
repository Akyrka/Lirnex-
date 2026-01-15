from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Dialog(models.Model):
    users = models.ManyToManyField(User)
    update_at = models.DateTimeField(auto_now=True)
    
class Message(models.Model):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    