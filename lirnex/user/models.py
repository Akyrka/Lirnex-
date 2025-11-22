from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=120,blank=True, null=True)
    photo_profile = models.ImageField(upload_to='profile_photos/',  default='profile_photos/default.png',blank=True)
    birthday = models.DateField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

#class CurrentStories(models.Model):

    
