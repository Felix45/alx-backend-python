from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    ''' Signal to create a notification when a new message is saved. '''
    if created:
        Notification.objects.create(
            user=instance.recipient,
            message=instance
        )
        print(f'Notification created for {instance.recipient.username} regarding new message from {instance.sender.username}.')

@receiver(pre_save, sender=Message)
def create_message_history(sender, instance, **kwargs):
    ''' Signal to create a message history entry when a message is about to be saved. '''
    if instance.id:
        MessageHistory.objects.create(
            message=instance,
            content=sender.objects.get(id=instance.id).content if instance.content else ''
        )