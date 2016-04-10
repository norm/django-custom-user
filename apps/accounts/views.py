from django.conf import settings
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    REDIRECT_FIELD_NAME,
    update_session_auth_hash,
)
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, TemplateView

from .forms import AuthenticationForm, NewAccountForm


class AccountView(TemplateView):
    template_name = 'accounts/account.html'


class ChangePasswordView(FormView):
    template_name = 'accounts/change_password.html'
    form_class = PasswordChangeForm

    def get_form(self):
        return PasswordChangeForm(
            user=self.request.user,
            data=self.request.POST,
        )

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super(ChangePasswordView, self).form_valid(form)

    def get_success_url(self):
        return reverse('accounts:password_changed')
        # redirect_to = self.request.POST.get(
        #     self.redirect_field_name,
        #     self.request.GET.get(self.redirect_field_name)
        # )
        # if not is_safe_url(url=redirect_to, host=self.request.get_host()):
        #     redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        # return redirect_to


class LoginView(FormView):
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'accounts/login.html'

    @method_decorator(never_cache)
    @method_decorator(sensitive_post_parameters())
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(LoginView, self).get_context_data(*args, **kwargs)
        context[self.redirect_field_name] = self.get_success_url()
        return context

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name)
        )
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        return redirect_to


class LogoutView(TemplateView):
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'accounts/logout.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LogoutView, self).get_context_data(*args, **kwargs)
        context[self.redirect_field_name] = self.get_success_url()
        return context

    def get_success_url(self):
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name)
        )
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = resolve_url(settings.LOGOUT_REDIRECT_URL)
        return redirect_to

    def post(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(self.get_success_url())


class NewAccountView(FormView):
    form_class = NewAccountForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'accounts/new.html'

    def get_success_url(self):
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name)
        )
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        return redirect_to

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return super(NewAccountView, self).form_valid(form)


class PasswordChangedView(TemplateView):
    template_name = 'accounts/password_changed.html'
