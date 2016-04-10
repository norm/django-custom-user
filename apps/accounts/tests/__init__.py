from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse


class AccountDetailsMixin(object):
    EMAIL = 'user@example.com'
    PASSWORD = 'correct horse battery staple'
    INCORRECT_PASSWORD = 'incorrect horse'
    FULL_NAME = 'Wendy Testaburger'
    FAMILIAR_NAME = 'Wends'


class AccountTestMixin(AccountDetailsMixin):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email=cls.EMAIL,
            password=cls.PASSWORD,
        )

    def login_user(self):
        form = self.app.get(reverse('accounts:login')).form
        form['email'] = self.EMAIL
        form['password'] = self.PASSWORD
        form.submit()
