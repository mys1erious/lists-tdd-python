from django.conf import settings
from django.contrib.auth import (
    BACKEND_SESSION_KEY,
    SESSION_KEY,
    get_user_model
)
from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest


User = get_user_model()


class MyListsTest(FunctionalTest):
    def create_pre_auth_session(self, email):
        user = User.objects.create(email=email)

        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        ## To set a cookie we need to first visit the domain.
        ## 404 page loads the quickest!
        self.browser.get(self.live_server_url+'/404_no_such_url/')
        self.browser.add_cookie({
            'name': settings.SESSION_COOKIE_NAME,
            'value': session.session_key,
            'path': '/'
        })

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'
        self.browser.get(self.live_server_url)
        self.wait_for_logout(email)

        self.create_pre_auth_session(email)
        self.browser.get(self.live_server_url)
        self.wait_for_login(email)
