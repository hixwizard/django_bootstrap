from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone
from django.utils.timezone import now
from core.constants import START_PAGE_NUM


def paginate(post_list, request, posts_to_display):
    page_number = request.GET.get('page', START_PAGE_NUM)
    paginator = Paginator(post_list, posts_to_display)
    return paginator.get_page(page_number)


def filter_posts(queryset):
    return queryset.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).select_related(
        'author',
        'location',
        'category'
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')


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


def get_annotated_posts(queryset):
    return queryset.posts.annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date').select_related('category', 'author', 'location')


def filter_published_posts(queryset):
    return queryset.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=now()
    )
