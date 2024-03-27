from django.db.models import Count
from django.utils import timezone


def publication_filters(queryset):
    """Применяет дополнительные фильтры публикации к queryset."""
    filters = {
        'is_published': True,
        'pub_date__lte': timezone.now()
    }

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
