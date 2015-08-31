from __future__ import unicode_literals

from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import MinLengthValidator
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


class SignupForm(forms.Form):
    email = forms.EmailField(label=_("email"))

    def form_valid(self):
        models.Code.objects.create(

        )


class SetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    password = forms.CharField(label=_("password"), widget=forms.PasswordInput,
                               validators=[
                                   MinLengthValidator(6),
                               ], help_text=_("Minimum 6 characters"))
    password2 = forms.CharField(label=_("password confirmation"),
                                widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2


class UserDisplayNamesForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            'hebrew_display_name',
            'english_display_name',
        )


class UserNoteForm(forms.ModelForm):
    # send_to_user = forms.BooleanField(required=False, label=_("send to user by email"))

    class Meta:
        model = models.UserNote
        fields = (
            'content',
            'visible_to_user',
            'is_open',
        )
