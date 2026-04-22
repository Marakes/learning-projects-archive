import pytest
from django.conf import settings

from news.forms import CommentForm


pytestmark = pytest.mark.django_db


def test_news_count(all_news, client, url_home):
    response = client.get(url_home)
    news_count = response.context['object_list'].count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(all_news, client, url_home):
    response = client.get(url_home)
    all_dates = [new.date for new in response.context['object_list']]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(url_detail, client, all_comments):
    response = client.get(url_detail)
    assert 'news' in response.context
    all_comments = response.context['news'].comment_set.all()
    timestamps = [comment.created for comment in all_comments]
    assert timestamps == sorted(timestamps)


def test_anonymous_client_has_no_form(url_detail, client):
    response = client.get(url_detail)
    assert 'form' not in response.context


def test_authed_client_has_form(url_detail, not_author_client):
    response = not_author_client.get(url_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
