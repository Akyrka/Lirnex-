from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.


#сделать модель для публикаций в главной ленте

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)




    def __str__(self):
        return f"Post by {self.author.username}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    context = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='uploads/', null=True, blank=True)


    def is_image(self):
        return self.file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))

    def is_video(self):
        return self.file.name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm'))

    def __str__(self):
        return f"Media for Post {self.post.id}"
@receiver(post_delete, sender=Media)
def delete_media_file(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(False)
    
# class Stories(models.Model):


# class Reels(models.Model):
    # video = 
