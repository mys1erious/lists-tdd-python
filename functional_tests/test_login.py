import os
import poplib
import re
import time

from django.core import mail
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


SUBJECT = 'Your login link for Lists-tdd'


class LoginTest(FunctionalTest):
    def test_can_get_email_link_to_login(self):
        # Edith goes to the awesome superlists site and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        if self.staging_server:
            test_email = 'lists.tdd.bot@gmail.com'
        else:
            test_email = 'skillcraba@gmail.com'

        self.browser.get(self.live_server_url)
        self.browser.find_element(by=By.NAME, value='email').send_keys(test_email)
        self.browser.find_element(by=By.NAME, value='email').send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element(by=By.TAG_NAME, value='body').text
        ))

        # She checks her email and finds a message
        body = self.wait_for_email(test_email, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Couldnt find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks it
        self.browser.get(url)

        # She is logged in
        self.wait_for_login(email=test_email)

        # Now she logs out
        self.browser.find_element(by=By.LINK_TEXT, value='Log out').click()

        # She is logged out
        self.wait_for_logout(email=test_email)

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.googlemail.com', 995)
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['STAGING_MAIL_PASS'])

            while time.time() - start < 60:
                # get 10 newest messages
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count-10), count+1)):
                    _, lines, _ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()
