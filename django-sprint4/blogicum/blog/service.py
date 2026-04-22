from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone

from blog.models import Post


def get_posts_for_object(
        posts=None, filtering=True, ordering='-pub_date', comments=True):
    """Получение постов с опциональной фильтрацией."""
    posts = posts or Post.objects
    posts = posts.select_related('category', 'location', 'author')

    if filtering:
        posts = posts.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )

    if ordering:
        posts = posts.order_by(ordering)

    if comments:
        posts = posts.annotate(comment_count=Count('comments'))

    return posts


def paginate_func(request, post_list, obj_numb):
    page_number = request.GET.get('page')
    return Paginator(post_list, obj_numb).get_page(page_number)
