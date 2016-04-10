from django.conf.urls import url

from apps.accounts.views import (
    AccountView,
    LoginView,
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
]
