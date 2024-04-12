from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, ActivityLog, Transaction


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=UserProfile)
def log_user_activity(sender, instance, created, **kwargs):
    action = 'Створено новий користувач' if created else 'Оновлено профіль користувача'
    ActivityLog.objects.create(user=instance.user, action=action)


@receiver(post_save, sender=Transaction)
def assign_user_to_transaction(sender, instance, created, **kwargs):
    action = f'Створено новий платіж на суму {instance.amount} від {instance.user}'
    ActivityLog.objects.create(user=instance.user, action=action)
