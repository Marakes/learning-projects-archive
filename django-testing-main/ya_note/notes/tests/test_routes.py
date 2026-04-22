from http import HTTPStatus

from notes.tests.fixtures import Fixtures


class TestRoutes(Fixtures):

    def test_home_page_for_anon_user(self):
        urls = (
            self.url_home,
            self.url_login,
            self.url_signup,
        )
        for name in urls:
            with self.subTest(name=name):
                response = self.client.get(name)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_logout_for_anon_user(self):
        response = self.client.post(self.url_logout)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        urls = (
            self.url_list,
            self.url_add,
            self.url_success,
        )
        for name in urls:
            with self.subTest(name=name):
                response = self.reader_client.get(name)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_detail_update_notes_different_user(self):
        users_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.reader_client, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            for name in (self.url_detail, self.url_edit, self.url_delete):
                with self.subTest(user=user, name=name):
                    response = user.get(name)
                    self.assertEqual(response.status_code, status)

    def test_availability_pages_for_anon_user(self):
        urls = (
            self.url_list,
            self.url_success,
            self.url_add,
            self.url_detail,
            self.url_edit,
            self.url_delete,
        )
        for name in urls:
            with self.subTest(name=name):
                redirect_url = f'{self.url_login}?next={name}'
                response = self.client.get(name)
                self.assertRedirects(response, redirect_url)
                response = self.client.post(name)
                self.assertRedirects(response, redirect_url)
