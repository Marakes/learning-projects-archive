from http import HTTPStatus as Hs

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, status',
    (
        (lf('url_home'), lf('client'), Hs.OK),
        (lf('url_login'), lf('client'), Hs.OK),
        (lf('url_signup'), lf('client'), Hs.OK),
        (lf('url_detail'), lf('client'), Hs.OK),
        (lf('edit_url'), lf('not_author_client'), Hs.NOT_FOUND),
        (lf('delete_url'), lf('not_author_client'), Hs.NOT_FOUND),
        (lf('edit_url'), lf('author_client'), Hs.OK),
        (lf('delete_url'), lf('author_client'), Hs.OK),
    ),
)
def test_pages_availability_for_anonymous_user(
        reverse_url, parametrized_client, status
):
    response = parametrized_client.get(reverse_url)
    assert response.status_code == status


def test_logout_page_availability_for_anonymous_user(client, url_logout):
    response = client.post(url_logout)
    assert response.status_code == Hs.OK


@pytest.mark.parametrize(
    'name',
    (
        lf('edit_url'),
        lf('delete_url'),
    ),
)
def test_redirects_for_anonymous_user(name, client):
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={name}'
    response = client.get(name)
    assertRedirects(response, expected_url)
