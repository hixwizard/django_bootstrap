from django.db.models import Count
from django.utils.timezone import now


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
