from __future__ import unicode_literals

from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
import floppyforms as forms


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


class CustomAuthenticationForm(forms.Form, AuthenticationForm):
    username = forms.CharField(max_length=254, widget=BetterEmailInput)
    password = forms.CharField(label=_("Password"),
                               widget=BetterPasswordInput)


class ImportUsersForm(forms.Form):
    program = forms.ModelChoiceField(Program.objects.all(),
                                     label=_("Program"),
                                     widget=forms.Select)
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput)
    text = forms.CharField(label=_("TSV Text"), widget=forms.Textarea,
                           help_text=_("First row must be columns, and should"
                                       " contain email and name"))
