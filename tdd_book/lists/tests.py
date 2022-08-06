from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve
from .views import home_page


class HomePage(TestCase):
    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_uses_home_template(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertIn('home.html', html)

    def test_can_save_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
