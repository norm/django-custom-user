from django.conf.urls import url

from apps.accounts.views import (
    AccountView,
    ChangePasswordView,
    LoginView,
    LogoutView,
    NewAccountView,
    PasswordChangedView,
)


urlpatterns = [
    url(
        r'^$',
        AccountView.as_view(),
        name='account',
    ),
    url(
        r'^login$',
        LoginView.as_view(),
        name='login',
    ),
    url(
        r'^logout$',
        LogoutView.as_view(),
        name='logout',
    ),
    url(
        r'^new$',
        NewAccountView.as_view(),
        name='new',
    ),
    url(
        r'^change-password$',
        ChangePasswordView.as_view(),
        name='change_password',
    ),
    url(
        r'^password-changed$',
        PasswordChangedView.as_view(),
        name='password_changed',
    ),
]
