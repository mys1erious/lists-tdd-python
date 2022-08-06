from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve
from .views import home_page


class HomePage(TestCase):
    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')

        html = response.content.decode('utf8')
        expected_html = render_to_string('home.html')
        self.assertEqual(html, expected_html)
