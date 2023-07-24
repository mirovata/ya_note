from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestProfileList(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Постящий')
        cls.other_author = User.objects.create(username='Второй постящий')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.other_author_client = Client()
        cls.other_author_client.force_login(cls.other_author)
        cls.note = Note.objects.create(
            title='Тестовая новость', text='Просто текст.', author=cls.author
        )

    def test_note_in_list_for_author(self):
        url = reverse('notes:list')
        response = self.author_client.get(url)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_note_not_in_list_for_another_user(self):
        url = reverse('notes:list')
        response = self.other_author_client.get(url)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_authorized_client_has_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.author_client.get(url)
                self.assertIsInstance(response.context['form'], NoteForm)
                self.assertIn('form', response.context)
