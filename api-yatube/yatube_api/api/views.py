from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class AuthorPermissionMixin:
    """Миксин для проверки прав автора."""

    def check_author_permissions(self, obj):
        # Пробовал решить через permissions, но не прошли тесты...
        if obj.author != self.request.user:
            raise PermissionDenied(
                'Изменение/Удаление чужого контента запрещено!'
            )


class PostViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    """Вьюсет для работы с постами, CRUD."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        self.check_author_permissions(serializer.instance)
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        self.check_author_permissions(instance)
        super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с группами, только GET."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями, CRUD."""

    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_pk'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.get_post()
        )

    def perform_update(self, serializer):
        self.check_author_permissions(serializer.instance)
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        self.check_author_permissions(instance)
        super().perform_destroy(instance)
