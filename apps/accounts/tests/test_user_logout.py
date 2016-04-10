from django.core.urlresolvers import reverse

from django_webtest import WebTest

from . import AccountTestMixin


class UserLogoutWebTest(AccountTestMixin, WebTest):
    def test_logout_is_in_navigation(self):
        self.login_user()
        page = self.app.get(reverse('homepage'))
        self.assertTrue(
            page.html.find('li', class_='logout')
        )

    def test_can_logout(self):
        self.login_user()

        form = self.app.get(reverse('accounts:logout')).forms['logout']
        response = form.submit()
        self.assertRedirects(response, '/')

        page = response.follow()
        self.assertTrue(
            page.html.find('li', class_='login')
        )

    def test_logout_respects_next_param(self):
        self.login_user()

        redirect_to = reverse('accounts:login')

        url = '%s?next=%s' % (
            reverse('accounts:logout'),
            redirect_to
        )

        form = self.app.get(url).forms['logout']
        response = form.submit()
        self.assertRedirects(response, redirect_to)

        page = response.follow()
        self.assertTrue(
            page.html.find('li', class_='login')
        )
