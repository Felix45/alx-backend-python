# views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Prefetch

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')

def get_threaded_messages(request):
    messages = (
        Message.objects
        .filter(receiver=request.user, parent_message__isnull=True)
        .select_related('sender', 'receiver')
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )
        .order_by('-timestamp')
    )
    return messages


def get_thread(message):
    thread = []
    replies = message.replies.select_related('sender').all()
    for reply in replies:
        thread.append({
            'message': reply,
            'replies': get_thread(reply)
        })
    return thread

@login_required
def inbox(request):
    unread_messages = Message.unread.for_user(request.user)
    return render(request, 'inbox.html', {'messages': unread_messages})