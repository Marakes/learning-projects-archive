from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class Fixtures(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.author = User.objects.create(username='author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='reader')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='my-slug',
            author=cls.author,
        )
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }

        cls.url_home = reverse('notes:home')
        cls.url_list = reverse('notes:list')
        cls.url_success = reverse('notes:success')
        cls.url_detail = reverse('notes:detail', args=(cls.note.slug,))
        cls.url_add = reverse('notes:add')
        cls.url_edit = reverse('notes:edit', args=(cls.note.slug,))
        cls.url_delete = reverse('notes:delete', args=(cls.note.slug,))
        cls.url_login = reverse('users:login')
        cls.url_logout = reverse('users:logout')
        cls.url_signup = reverse('users:signup')
