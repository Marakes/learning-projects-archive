from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import Truncator

from posts.constants import TRUNCATE_TEXT


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return Truncator(self.title).chars(TRUNCATE_TEXT)


class Post(models.Model):
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Группа',
        related_name='posts'
    )

    def __str__(self):
        # Добавил default_related_name = 'posts', но тесты не пропустили
        return Truncator(self.text).chars(TRUNCATE_TEXT)


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
        related_name='comments'
    )
    text = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        # Добавил default_related_name = 'comments', но тесты не пропустили
        return (f'Текст: {Truncator(self.text).chars(TRUNCATE_TEXT)}. '
                f'Автор: {self.author}. Пост: {self.post}')
