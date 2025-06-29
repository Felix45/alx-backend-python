# Generated by Django 4.2.23 on 2025-06-15 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('signals', '0003_message_edited_messagehistory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messagehistory',
            old_name='timestamp',
            new_name='edited_at',
        ),
        migrations.AddField(
            model_name='messagehistory',
            name='edited_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='edited_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
