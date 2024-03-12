from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post
from .models import Comment

class YourRegistrationForm(UserCreationForm):
    # Если у вас есть дополнительные поля для регистрации, добавьте их здесь

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']  # Это минимальный набор полей для регистрации


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
