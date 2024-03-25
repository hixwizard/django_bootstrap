from typing import List

from django.contrib import admin

from .models import Category, Location, Post, Comment

admin.site.empty_value_display = 'Не задано'


class CategoryAdmin(admin.ModelAdmin):
    """Административная панель для управления Категориями."""

    list_display: List[str] = (
        'title',
        'description',
        'slug',
        'is_published'
    )


class LocationAdmin(admin.ModelAdmin):
    """Административная панель для управления Местположением."""

    list_display: List[str] = (
        'name',
        'is_published'
    )


class PostAdmin(admin.ModelAdmin):
    """Административная панель для управления Постами."""

    list_display: List[str] = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )


class CommentAdmin(admin.ModelAdmin):
    """Административная панель для управления Комментариями."""

    list_display: List[str] = (
        'text',
        'post',
        'created_at',
        'author'
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
