from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .basic import *
from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        new_post_subscription(instance)
