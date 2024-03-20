from django import forms
from django.contrib.auth.models import User

from .models import Comment, Post


class UserEditForm(forms.ModelForm):
    """Форма для редактирования пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class CommentForm(forms.ModelForm):
    """Форма для комментария."""

    class Meta:
        model = Comment
        fields = ['text']


class PostForm(forms.ModelForm):
    """Форма для поста."""

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'text': forms.Textarea(),
            'comment': forms.Textarea(),
            'pub_date': forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={'type': 'datetime-local'}),
        }
