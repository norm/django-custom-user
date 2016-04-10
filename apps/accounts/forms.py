from django import forms
from django.contrib.auth import (
    authenticate, password_validation,
)
from django.utils.translation import ugettext_lazy as _

from .models import User


class AuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': ''}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _(
            'Please enter a correct email address and password. '
            'Note that both fields may be case-sensitive.'
        ),
        'inactive': _('This account is inactive.'),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class NewAccountForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_('Enter the same password as before, for verification.')
    )
    full_name = forms.CharField(label=_('Full name'), required=False)
    familiar_name = forms.CharField(label=_('Familiar name'), required=False)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'familiar_name')

    def __init__(self, *args, **kwargs):
        super(NewAccountForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': ''})

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.email = self.cleaned_data.get('email')
        password_validation.validate_password(
            self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(NewAccountForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
