from django.core.urlresolvers import reverse

from django_webtest import WebTest

from . import AccountDetailsMixin


class UserLogoutWebTest(AccountDetailsMixin, WebTest):
    def test_new_account_is_in_navigation(self):
        page = self.app.get(reverse('homepage'))
        self.assertFalse(
            page.html.find('li', class_='user')
        )
        self.assertTrue(
            page.html.find('li', class_='new')
        )

    def test_cannot_create_new_account_without_password(self):
        form = self.app.get(reverse('accounts:new')).forms['new']
        form['email'] = self.EMAIL
        response = form.submit()
        errors = response.html.find('ul', class_='errorlist')

        self.assertTrue('new' in response.forms)
        self.assertEqual(errors.find('li').text, 'This field is required.')

    def test_cannot_create_new_account_without_email(self):
        form = self.app.get(reverse('accounts:new')).forms['new']
        form['password1'] = self.PASSWORD
        form['password1'] = self.PASSWORD
        response = form.submit()
        errors = response.html.find('ul', class_='errorlist')

        self.assertTrue('new' in response.forms)
        self.assertEqual(errors.find('li').text, 'This field is required.')

    def test_can_create_new_account_without_names(self):
        form = self.app.get(reverse('accounts:new')).forms['new']
        form['email'] = self.EMAIL
        form['password1'] = self.PASSWORD
        form['password2'] = self.PASSWORD
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
            self.EMAIL
        )

        names = response.html.findAll('dd', class_='name')
        for name in names:
            self.assertEqual(name.text, 'Not set')

    def test_can_create_new_account_with_names(self):
        form = self.app.get(reverse('accounts:new')).forms['new']
        form['email'] = self.EMAIL
        form['password1'] = self.PASSWORD
        form['password2'] = self.PASSWORD
        form['familiar_name'] = self.FAMILIAR_NAME
        form['full_name'] = self.FULL_NAME
        response = form.submit()
        self.assertRedirects(response, reverse('accounts:account'))

        response = response.follow()
        names = response.html.findAll('dd', class_='name')

        self.assertEqual(
            response.html.find('h1').text,
            self.EMAIL
        )
        self.assertEqual(names[0].text, self.FULL_NAME)
        self.assertEqual(names[1].text, self.FAMILIAR_NAME)

    def test_create_new_account_respects_next_param(self):
        url = '%s?next=/' % reverse('accounts:new')
        form = self.app.get(url).forms['new']
        form['email'] = self.EMAIL
        form['password1'] = self.PASSWORD
        form['password2'] = self.PASSWORD
        form['familiar_name'] = self.FAMILIAR_NAME
        form['full_name'] = self.FULL_NAME
        response = form.submit()
        self.assertRedirects(response, '/')
