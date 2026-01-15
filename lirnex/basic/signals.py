from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed

from .models import Post, Comment, Notification
from user.models import Profile  


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.user != instance.post.author:
        Notification.objects.create(
            to_user=instance.post.author,
            from_user=instance.user,   # хранится, но не выводится
            notif_type="comment",
            post=instance.post,
            text=instance.text        # ← ТОЛЬКО ТЕКСТ
        )




@receiver(m2m_changed, sender=Post.likes.through)
def create_like_notification(sender, instance, action, reverse, pk_set, **kwargs):
    if action == "post_add":  # лайк добавлен
        for pk in pk_set:
            user = User.objects.get(pk=pk)  # тот кто лайкнул

            if user != instance.author: 
                Notification.objects.create(
                    to_user=instance.author,
                    from_user=user,
                    notif_type="like",
                    post=instance,
                    text=f"{user.username} лайкнул ваш пост"
                )



@receiver(m2m_changed, sender=Profile.following.through)
def follow_notification(sender, instance, action, reverse, pk_set, **kwargs):
    if action == "post_add":
        for pk in pk_set:
            followed_user = User.objects.get(pk=pk)
            Notification.objects.create(
                to_user=followed_user,
                from_user=instance.user,
                notif_type="follow",
                text=f"{instance.user.username} подписался на вас"
            )
