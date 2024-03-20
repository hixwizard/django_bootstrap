from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth.models import User
from models import Post
from django.utils import timezone


def get_author(username):
    return get_object_or_404(User, username=username)


def get_user_posts(author, request_user):
    posts = author.posts.annotate(
        comment_count=Count('comments')
    ).order_by(
        '-pub_date').select_related(
            'category',
            'author',
            'location'
    )
    if author != request_user:
        posts = posts.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=now()
        )
    return posts


def get_published_posts():
    return Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).select_related(
        'author',
        'location',
        'category'
    ).annotate(comment_count=Count('comments')).order_by(
        '-pub_date'
    )
