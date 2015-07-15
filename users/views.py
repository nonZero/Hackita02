from email.utils import parseaddr

import authtools.views
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView
from django.utils.translation import ugettext_lazy as _

from . import forms
from users.base_views import ProtectedMixin


class LoginView(authtools.views.LoginView):
    template_name = "users/login.html"
    form_class = forms.LoginForm


# class SignupView(FormView):
#     template_name = "users/signup.html"
#     form_class = forms.SignupForm


class LogoutView(authtools.views.LogoutView):
    url = reverse_lazy(settings.LOGIN_URL)


class ValidationSentView(TemplateView):
    template_name = "users/validation-sent.html"

    def get(self, request, *args, **kwargs):
        self.email = request.session.get('email_validation_address')
        self.from_email = parseaddr(settings.EMAIL_FROM)[1]
        if not self.email:
            return redirect("home")
        return super().get(request, *args, **kwargs)


class SetPasswordView(FormView):
    template_name = "users/set-password.html"
    form_class = forms.SetPasswordForm
    success_url = reverse_lazy("sa:dashboard")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.has_password():
            return HttpResponseBadRequest("400 BAD REQUEST Password already set")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.user.set_password(form.cleaned_data['password'])
        self.request.user.save()
        update_session_auth_hash(self.request, self.request.user)
        messages.success(self.request, _("Password was set succesfully"))
        return super().form_valid(form)
