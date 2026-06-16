# subscriptions/apps.py
from django.apps import AppConfig

class SubscriptionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "subscriptions"

    def ready(self):
        # This forces Django to read your tasks.py file on startup!
        import subscriptions.tasks