from django.core.paginator import Paginator

from core.constants import START_PAGE_NUM


def paginate(post_list, request, posts_to_display):
    page_number = request.GET.get('page', START_PAGE_NUM)
    paginator = Paginator(post_list, posts_to_display)
    return paginator.get_page(page_number)
