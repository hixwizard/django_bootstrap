from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.timezone import now


def paginate(post_list, page_number, posts_to_display):
    paginator = Paginator(post_list, posts_to_display)
    return paginator.get_page(page_number)


def filter_posts_by_category(queryset, category_slug):
    return queryset.filter(
        category__slug=category_slug,
        pub_date__lte=timezone.now(),
        is_published=True
    ).select_related(
        'author',
        'location',
        'category',
    ).order_by('-pub_date')


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
