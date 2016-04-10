from django.conf.urls import url

from apps.accounts.views import (
    AccountView,
    LoginView,
    LogoutView,
    NewAccountView,
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
]
