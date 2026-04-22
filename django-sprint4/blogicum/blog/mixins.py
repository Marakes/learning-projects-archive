from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from blog.models import Post


class OnlyAuthorMixin:
    """Миксин подтверждения авторства и пересылки на страницу поста."""

    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return redirect('blog:post_detail', post_id=obj.pk)
        return super().dispatch(request, *args, **kwargs)


class PostModelMixin(LoginRequiredMixin):
    """Миксин с указанием модели поста и шаблона для поста."""

    model = Post
    template_name = 'blog/create.html'
