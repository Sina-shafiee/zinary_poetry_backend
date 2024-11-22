from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def add_to_basic_user_group(sender, instance, created, **kwargs):
    if created and not instance.groups.exists():
        basic_user_group, _ = Group.objects.get_or_create(name="Basic User")
        instance.groups.add(basic_user_group)
