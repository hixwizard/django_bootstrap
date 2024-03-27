from django.contrib import admin

from .models import Category, Comment, Location, Post

admin.site.empty_value_display = 'Не задано'


class CategoryAdmin(admin.ModelAdmin):
    """Административная панель для управления Категориями."""

    list_display = (
        'title',
        'description',
        'slug',
        'is_published'
    )


class LocationAdmin(admin.ModelAdmin):
    """Административная панель для управления Местположением."""

    list_display = (
        'name',
        'is_published'
    )


class PostAdmin(admin.ModelAdmin):
    """Административная панель для управления Постами."""

    list_display = (
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
    """Административная панель для управления комментариями."""

    list_display = (
        'text',
        'post',
        'created_at',
        'author'
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
