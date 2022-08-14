from django.conf import settings

from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session



class MyListsTest(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        ## To set a cookie we need to first visit the domain.
        ## 404 page loads the quickest!
        self.browser.get(self.live_server_url+'/404_no_such_url/')
        self.browser.add_cookie({
            'name': settings.SESSION_COOKIE_NAME,
            'value': session_key,
            'path': '/'
        })

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'
        self.browser.get(self.live_server_url)
        self.wait_for_logout(email)

        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_for_login(email)
