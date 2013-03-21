from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.utils import override_settings


@override_settings(LANGUAGE_CODE='en-en')
class MiniTwitTestCase(TestCase):

    def SetUp(self):
        """Before each test, set up a blank database"""
        self.client = Client()

    def register(self, username, password, password2=None, email=None):
        """Helper function to register a user"""
        if password2 is None:
            password2 = password
        if email is None:
            email = username + '@example.com'
        return self.client.post(reverse('register'), data={
            'username': username,
            'password1': password,
            'password2': password2,
            'email': email,
        }, follow=True)

    # Tests

    def test_user_register(self):
        response = self.register('user1', 'default')
        self.assertContains(response, 'You were successfully registered ' \
                'and can login now')
        self.assertEqual(len(response.context['messages']), 1)
        response = self.register('user1', 'default')
        self.assertContains(response, 'Ya existe un usuario con este nombre') #'The username is already taken')
        #TODO Completar el text teniendo en cuenta el idioma local


    def test_user_login(self):
        pass

    def test_user_logout(self):
        pass

    def test_user_follow(self):
        #only post
        pass

    def test_user_unfollow(self):
        #only post
        pass

    def test_timeline_self(self):
        #pagination
        #title
        #followed users
        pass

    def test_timeline_public(self):
        #pagination
        pass

    def test_timeline_user(self):
        pass

    def test_post_message(self):
        #only post
        pass
