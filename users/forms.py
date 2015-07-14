from __future__ import unicode_literals

from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
import floppyforms.__future__ as forms
from . import models


class BetterEmailInput(forms.EmailInput):
    def get_context(self, name, value, attrs=None):
        ctx = super(BetterEmailInput, self).get_context(name, value,
                                                        attrs)
        ctx['attrs']['placeholder'] = 'email address'
        return ctx


class BetterPasswordInput(forms.PasswordInput):
    def get_context(self, name, value, attrs=None):
        ctx = super(BetterPasswordInput, self).get_context(name, value,
                                                           attrs)
        ctx['attrs']['placeholder'] = 'password'
        return ctx


class LoginForm(forms.Form, AuthenticationForm):
    username = forms.CharField(max_length=254, widget=BetterEmailInput)
    password = forms.CharField(label=_("Password"),
                               widget=BetterPasswordInput)


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = models.PersonalInfo
        exclude = (
            'user',
        )
        # fields = (
        #     'hebrew_first_name',
        #     'hebrew_last_name',
        #     'english_first_name',
        #     'english_last_name',
        #     'main_phone',
        #     'alt_phone',
        #     'city',
        #     'address',
        #     'gender',
        #     'skype_username',
        # )
