from django.conf.urls import url

from apps.accounts.views import (
    AccountView,
)


urlpatterns = [
    url(
        r'^$',
        AccountView.as_view(),
        name='account',
    ),
]
