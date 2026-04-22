from notes.forms import NoteForm
from notes.tests.fixtures import Fixtures


class TestContent(Fixtures):

    def test_note_appears_in_list_for_author(self):
        response = self.author_client.get(self.url_list)
        notes = response.context['object_list']
        self.assertTrue(self.note in notes)

    def test_only_author_sees_own_note(self):
        users_see_notes = (
            (self.author_client, self.assertIn),
            (self.reader_client, self.assertNotIn),
        )
        for user, assertion in users_see_notes:
            with self.subTest(user=user):
                response = user.get(self.url_list)
                notes = response.context['object_list']
                assertion(self.note, notes)

    def test_form_passed_to_add_and_edit_pages(self):
        urls = (
            self.url_add,
            self.url_edit,
        )
        for name in urls:
            with self.subTest(name=name):
                response = self.author_client.get(name)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
