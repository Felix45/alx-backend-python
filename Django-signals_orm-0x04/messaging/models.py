from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    ''' A model representing a message in the system. '''

    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    edited  = models.BooleanField(default=False, help_text="Indicates if the message has been edited.")
    parent_message = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}'


class Notification(models.Model):
    ''' A model representing a notification for a user. '''

    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.username} regarding message from {self.message.sender.username}'
    
class MessageHistory(models.Model):
    ''' A model representing the history of a message. '''

    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, related_name='edited_messages', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'History for message {self.message.id} at {self.edited_at} {self.edited_by.username if self.edited_by else "System"}'

