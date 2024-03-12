from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Конфигурация приложения Блог."""

    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'blog'
    verbose_name: str = 'Блог'
