from django.apps import AppConfig

class MessagingConfig(AppConfig):
    """Configuration for the messaging app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'signals'

    def ready(self):
        """Import signals to ensure they are registered."""
        import signals.signals
