from django.contrib.auth import get_user_model
from django.db import models

from core.constants import MAX_CHARACTERS
from core.models import PublishedModel


User = get_user_model()


class Post(PublishedModel):
    """Определяет свойства поста."""

    title = models.CharField(
        max_length=MAX_CHARACTERS,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем'
                   ' — можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts'
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Местоположение',
        related_name='posts'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name='Категория',
        related_name='posts'
    )
    image = models.ImageField(
        blank=True,
        verbose_name='Изображение'
    )

    class Meta:
        """Дополнительные параметры для перевода."""

        verbose_name: str = 'публикация'
        verbose_name_plural: str = 'Публикации'

    def __str__(self) -> str:
        """Параметр для отображения названия."""
        return self.title[:15]


class Category(PublishedModel):
    """Определяет свойства категорий."""

    title = models.CharField(
        max_length=MAX_CHARACTERS,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; разрешены символы '
                   'латиницы, цифры, дефис и подчёркивание.'),
    )

    class Meta:
        verbose_name: str = 'категория'
        verbose_name_plural: str = 'Категории'

    def __str__(self) -> str:
        return self.title


class Location(PublishedModel):
    """Определяет свойства местоположения."""

    name = models.CharField(
        max_length=MAX_CHARACTERS,
        verbose_name='Название места',
    )

    class Meta:
        verbose_name: str = 'местоположение'
        verbose_name_plural: str = 'Местоположения'

    def __str__(self) -> str:
        return self.name


class Comment(PublishedModel):
    text = models.TextField(verbose_name='Текст комментария',)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ('created_at',)
