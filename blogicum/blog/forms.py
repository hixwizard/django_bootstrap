from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Post


class YourRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class YourPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'text', 'pub_date',
            'location', 'category', 'image'
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
