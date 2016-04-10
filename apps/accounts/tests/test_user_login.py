from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from django_webtest import WebTest


class UserWebTest(WebTest):
    EMAIL = 'user@example.com'
    PASSWORD = 'correct horse battery staple'
    INCORRECT_PASSWORD = 'incorrect horse'

    def test_login_in_navigation(self):
        page = self.app.get(reverse('homepage'))
        self.assertFalse(
            page.html.find('li', class_='user')
        )
        self.assertTrue(
            page.html.find('li', class_='login')
        )

    def test_can_login(self):
        get_user_model().objects.create_user(
            email=self.EMAIL,
            password=self.PASSWORD,
            is_active=True,
        )

        form = self.app.get(reverse('accounts:login')).form
        form['email'] = self.EMAIL
        form['password'] = self.PASSWORD
        response = form.submit()
        self.assertRedirects(response, reverse('accounts:account'))

        # the navigation changes once logged in
        response = response.follow()
        self.assertTrue(
            response.html.find('li', class_='user')
        )
        self.assertFalse(
            response.html.find('li', class_='login')
        )
        self.assertEqual(
            response.html.find('h1').text,
            'user@example.com'
        )

    def test_cannot_login_with_blank_form(self):
        form = self.app.get(reverse('accounts:login')).form
        response = form.submit()
        self.assertTrue('login' in response.forms)

        errors = response.html.findAll('ul', class_='errorlist')
        for error in errors:
            self.assertEquals(error.text, 'This field is required.')

    def test_cannot_login_with_wrong_password(self):
        form = self.app.get(reverse('accounts:login')).form
        form['email'] = self.EMAIL
        form['password'] = self.INCORRECT_PASSWORD
        response = form.submit()
        self.assertTrue('login' in response.forms)

        errors = response.html.findAll('ul', class_='errorlist')
        for error in errors:
            self.assertEquals(
                error.text,
                'Please enter a correct email address and password. '
                'Note that both fields may be case-sensitive.'
            )

    def test_login_respects_next_param(self):
        get_user_model().objects.create_user(
            email=self.EMAIL,
            password=self.PASSWORD,
            is_active=True,
        )

        url = '%s?next=/' % reverse('accounts:login')
        form = self.app.get(url).form
        form['email'] = self.EMAIL
        form['password'] = self.PASSWORD
        response = form.submit()

        self.assertRedirects(response, '/')
