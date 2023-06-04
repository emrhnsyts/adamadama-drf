from django.db.models.signals import post_save
from django.dispatch import receiver

from sessions.models import Session


@receiver(post_save, sender=Session)
def add_current_user_to_session(sender, instance, created, **kwargs):
    if created:
        instance.users.add(instance.owner)
