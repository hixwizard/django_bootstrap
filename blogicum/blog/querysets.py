from django.db.models import Count
from django.utils import timezone


def publication_filters(
        queryset, category_slug=None, author=None, published_only=False
):
    """Применяет дополнительные фильтры публикации к queryset."""
    filters = {
        'is_published': True,
        'category__is_published': True,
        'pub_date__lte': timezone.now()
    }
    if category_slug is not None:
        filters['category__slug'] = category_slug
    if author is not None:
        filters['author'] = author
    if published_only:
        queryset = queryset.filter(**filters)
    return queryset


def annotation_and_selects(queryset):
    """Применяет аннотации и select_related на queryset."""
    return queryset.annotate(
        comment_count=Count('comments')
    ).order_by(
        '-pub_date'
    ).select_related(
        'category', 'author', 'location'
    )
