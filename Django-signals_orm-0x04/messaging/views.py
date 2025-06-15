# views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Prefetch

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')

@login_required
def get_threaded_messages(request):
    messages = Message.objects.filter(sender=request.user) | Message.objects.filter(receiver=request.user)
    messages = (
        messages
        .select_related('sender', 'receiver', 'parent_message')
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver', 'parent_message'))
        )
        .order_by('-timestamp')
    )

    return messages
