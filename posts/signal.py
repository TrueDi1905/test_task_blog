from django.dispatch import receiver
from django.db.models import signals

from .models import Post, Follow
from .systems import send


@receiver(signals.post_save, sender=Post)
def send_mail(sender, instance, created, **kwargs):
    follows = Follow.objects.filter(author=instance.author)
    for follow in follows:
        send(follow.user, instance.author)
