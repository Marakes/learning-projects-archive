from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import (
    CreateView, DeleteView, ListView, UpdateView)

from blog.constants import PAGINATOR_NUMB
from blog.forms import CommentForm, PostForm
from blog.mixins import OnlyAuthorMixin, PostModelMixin
from blog.models import Category, Comment, Post
from blog.service import get_posts_for_object, paginate_func


User = get_user_model()


def index(request):
    """Обрабатывает запрос на главную страницу сайта."""
    post_list = get_posts_for_object()
    context = {
        'post_list': post_list,
        'page_obj': paginate_func(request, post_list, PAGINATOR_NUMB)
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """Обрабатывает запрос на страницу определённого поста."""
    post = get_object_or_404(
        get_posts_for_object(filtering=False),
        pk=post_id
    )
    if request.user != post.author:
        post = get_object_or_404(
            get_posts_for_object(),
            pk=post_id
        )
    form = CommentForm() if request.user.is_authenticated else None
    comments = post.comments.select_related(
        'author').order_by('created_at')
    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """Обрабатывает запрос на страницу категории постов."""
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    post_list = get_posts_for_object(posts=category.posts)
    context = {
        'category': category,
        'page_obj': paginate_func(request, post_list, PAGINATOR_NUMB)
    }
    return render(request, 'blog/category.html', context)


class PostCreateView(PostModelMixin, CreateView):
    """Обрабатывает запрос на создание поста."""

    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={
            'profile_slug': self.request.user.username
        })


class PostUpdateView(OnlyAuthorMixin, PostModelMixin, UpdateView):
    """Обрабатывает запрос на редактирование поста."""

    form_class = PostForm

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.pk}
        )


class PostDeleteView(OnlyAuthorMixin, PostModelMixin, DeleteView):
    """Обрабатывает запрос на удаление поста."""

    def get_success_url(self):
        return reverse('blog:profile', kwargs={
            'profile_slug': self.object.author.username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


class ProfileView(ListView):
    """Обрабатывает запрос на страницу профиля."""

    model = Post
    template_name = 'blog/profile.html'
    paginate_by = PAGINATOR_NUMB

    @cached_property
    def profile(self):
        return get_object_or_404(
            User,
            username=self.kwargs['profile_slug']
        )

    def get_queryset(self):
        return get_posts_for_object(
            posts=self.profile.posts,
            filtering=self.request.user != self.profile
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    """Обрабатывает запрос на изменение профиля."""

    model = User
    template_name = 'blog/user.html'
    fields = ['first_name', 'last_name', 'username', 'email']

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', kwargs={
            'profile_slug': self.object.username})


@login_required
def add_comment(request, post_id):
    """Обрабатывает запрос на добавление комментария."""
    post = get_object_or_404(
        Post,
        pk=post_id
    )

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Обрабатывает запрос на редактирование комментария."""
    comment = get_object_or_404(Comment, pk=comment_id, post_id=post_id)
    if comment.author != request.user:
        return HttpResponseForbidden('Not Not')

    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)

    context = {
        'form': form,
        'comment': comment,
        'post_id': post_id
    }
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    """Обрабатывает запрос на удаление комментария."""
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden('Not Not')

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', {'comment': comment})


class CustomLogoutView(LogoutView):
    """Обрабатывает запрос на выход из аккаунта."""

    http_method_names = ["get", "post", "options"]

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
