from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Post


class UserEditForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class PostForm(forms.ModelForm):

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
