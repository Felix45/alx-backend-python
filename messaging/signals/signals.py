from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    ''' Signal to create a notification when a new message is saved. '''
    if created:
        Notification.objects.create(
            user=instance.recipient,
            message=instance
        )
        print(f'Notification created for {instance.recipient.username} regarding new message from {instance.sender.username}.')