from django.db.models import Count
from django.utils.timezone import now
from .models import Post, Category
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from core.constants import POSTS_TO_DISPLAY
from django.utils import timezone


def get_posts_in_category(slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    post_list = Post.objects.filter(
        category=category,
        pub_date__lte=timezone.now(),
        is_published=True
    ).select_related(
        'author',
        'location',
        'category',
    ).order_by('-pub_date')

    paginator = Paginator(post_list, POSTS_TO_DISPLAY)
    posts = paginator.page(paginator.num_pages)

    return posts, category


def get_annotated_posts(author):
    return author.posts.annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date').select_related('category', 'author', 'location')


def filter_published_posts(posts, author, request_user):
    if author != request_user:
        return posts.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=now()
        )
    return posts
