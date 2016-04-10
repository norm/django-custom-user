from django.views.generic import TemplateView


class AccountView(TemplateView):
    template_name = 'accounts/account.html'
