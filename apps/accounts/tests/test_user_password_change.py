from django.core.urlresolvers import reverse

from django_webtest import WebTest

from . import AccountTestMixin


class UserLoginWebTest(AccountTestMixin, WebTest):
    NEW_PASSWORD = 'ribbon cruel aunt send'

    def test_no_action_with_incorrect_old_password(self):
        self.login_user()
        url = reverse('accounts:change_password')
        form = self.app.get(url).forms['password']
        form['old_password'] = self.INCORRECT_PASSWORD
        form['new_password1'] = self.NEW_PASSWORD
        form['new_password2'] = self.NEW_PASSWORD

        # the form is presented again
        response = form.submit()
        self.assertTrue('password' in response.forms)

        errors = response.html.find('ul', class_='errorlist')
        self.assertEquals(
            errors.find('li').text,
            'Your old password was entered incorrectly. Please enter it again.'
        )

    def test_can_change_password(self):
        self.login_user()
        url = reverse('accounts:change_password')
        form = self.app.get(url).forms['password']
        form['old_password'] = self.PASSWORD
        form['new_password1'] = self.NEW_PASSWORD
        form['new_password2'] = self.NEW_PASSWORD

        # works...
        response = form.submit()
        self.assertRedirects(response, reverse('accounts:password_changed'))

        response = response.follow()
        self.assertEquals(
            response.html.find('h1').text,
            'Your password was changed.'
        )

        # ...so we logout...
        url = reverse('accounts:logout')
        response = self.app.get(url).forms['logout'].submit()
        self.assertRedirects(response, '/')

        # ...and login again with the new password
        form = self.app.get(reverse('accounts:login')).form
        form['email'] = self.EMAIL
        form['password'] = self.NEW_PASSWORD
        response = form.submit()
        self.assertRedirects(response, reverse('accounts:account'))
