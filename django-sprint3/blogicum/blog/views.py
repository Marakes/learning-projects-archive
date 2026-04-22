from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .constants import POSTS_COUNT_ON_INDEX
from .models import Category, Post


def get_posts_for_object(obj_posts=None):
    """Фильтрация постов для объекта."""
    posts = obj_posts.all() if obj_posts is not None else Post.objects
    return posts.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )


def index(request):
    """Обрабатывает запрос на главную страницу сайта."""
    post_list = get_posts_for_object().order_by(
        '-pub_date'
    )[:POSTS_COUNT_ON_INDEX]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """Обрабатывает запрос на страницу определённого поста."""
    post = get_object_or_404(
        get_posts_for_object(),
        pk=post_id
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """Обрабатывает запрос на страницу категории постов."""
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    post_list = get_posts_for_object(category.posts)
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)
