from django.apps import AppConfig


class PagesConfig(AppConfig):
    """Конфигурация приложения Pages."""

    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'pages'
