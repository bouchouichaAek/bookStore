from django.apps import AppConfig


class PaimentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'paiment'

    def ready(self):
        import paiment.signals

