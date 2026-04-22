from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


pytestmark = pytest.mark.django_db


FORM_DATA = {'text': 'Новый комментарий'}


def test_anonymous_user_cant_create_comments(
        client, url_detail, url_to_comments
):
    comments_count_before = Comment.objects.count()
    client.post(url_detail, data=FORM_DATA)
    comments_count_after = Comment.objects.count()
    assert comments_count_before == comments_count_after


def test_authed_user_can_create_comments(
        author_client, news, author, url_detail, url_to_comments
):
    Comment.objects.all().delete()
    response = author_client.post(url_detail, data=FORM_DATA)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, url_detail):
    bad_words_data = {'text': f'Такой-то текст, {BAD_WORDS[0]}, еще текст'}
    comments_count_before = Comment.objects.count()
    response = author_client.post(url_detail, data=bad_words_data)
    comments_count_after = Comment.objects.count()
    assert comments_count_before == comments_count_after
    form = response.context['form']
    assertFormError(
        form=form,
        field='text',
        errors=WARNING
    )


def test_author_can_delete_comment(
        author_client, comment, delete_url, url_to_comments
):
    comments_count_before = Comment.objects.count()
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    assert response.status_code == HTTPStatus.FOUND
    comments_count_after = Comment.objects.count()
    assert comments_count_after == comments_count_before - 1


def test_not_author_cant_delete_comment(
        not_author_client, comment,
        delete_url, url_to_comments
):
    comments_count_before = Comment.objects.count()
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count_after = Comment.objects.count()
    assert comments_count_before == comments_count_after


def test_author_can_edit_comment(
        author_client, comment, news,
        edit_url, url_to_comments, author
):
    response = author_client.post(edit_url, data=FORM_DATA)
    assertRedirects(response, url_to_comments)
    assert response.status_code == HTTPStatus.FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == FORM_DATA['text']
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news


def test_not_author_can_edit_comment(
        not_author_client, comment, author_client,
        edit_url, url_to_comments, author, news
):
    response = not_author_client.post(edit_url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == comment.text
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news
