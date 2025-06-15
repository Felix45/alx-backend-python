from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    ''' Signal to create a notification when a new message is saved. '''
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
        print(f'Notification created for {instance.receiver.username} regarding new message from {instance.sender.username}.')

@receiver(pre_save, sender=Message)
def create_message_history(sender, instance, **kwargs):
    ''' Signal to create a message history entry when a message is about to be saved. '''
    if instance.id:
        MessageHistory.objects.create(
            message=instance,
            content=sender.objects.get(id=instance.id).content if instance.content else ''
        )

@receiver(post_delete, sender=User)
def cleanup_related_data(sender, instance, **kwargs):
    ''' Signal to clean up related data when a user is deleted. '''
    # Delete messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications directly related to the user
    Notification.objects.filter(user=instance).delete()

    # Delete message history related to messages sent/received by the user
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
