from email.utils import parseaddr

import authtools.views
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_managers
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView, View, UpdateView
from django.utils.translation import ugettext_lazy as _

from . import forms
from . import models
from hackita02.base_views import ProtectedViewMixin


class LoginView(authtools.views.LoginView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    page_title = _("Login")


class LogoutView(authtools.views.LogoutView):
    url = reverse_lazy(settings.LOGIN_URL)


class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignupForm
    page_title = _("Signup")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super(SignupView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        code = models.Code.objects.generate(email)
        base = self.request.build_absolute_uri("/")[:-1]
        code.send_validation(base)
        self.request.session['validation_sent_to'] = email

        return redirect("users:validation_sent")


class ValidationSentView(TemplateView):
    template_name = "users/validation-sent.html"
    page_title = _("Validation Sent")

    def get(self, request, *args, **kwargs):
        self.email = request.session.get('validation_sent_to')
        if not self.email:
            return redirect("home")

        self.from_email = parseaddr(settings.EMAIL_FROM)[1]
        return super().get(request, *args, **kwargs)


class ValidateView(View):
    def get(self, request, code, *args, **kwargs):
        try:
            o = models.Code.objects.get(code=code)
            if (
                        timezone.now() - o.created_at).days > settings.VALIDATE_LINK_DAYS:
                o.delete()
                messages.error(request, _(
                    "validation code too old. Please generate a new code"))
                return redirect("users:login")

        except models.Code.DoesNotExist:
            messages.error(request, _("Invalid validation code."))
            return redirect("users:login")

        try:
            user = models.User.objects.get(email=o.email)
            if not user.is_active:
                messages.error(request, _("Inactive user."))
                return redirect("users:login")
            messages.success(request, _("Welcome back!"))

        except models.User.DoesNotExist:
            user = models.User.objects.create_user(o.email)
            title = "New email User: {}".format(o.email)
            mail_managers(title, title)
            messages.success(request, _(
                "Welcome! You can set your password any time from the menu above."))

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        o.delete()
        return redirect(settings.LOGIN_REDIRECT_URL)


class SetPasswordView(FormView):
    template_name = "users/set-password.html"
    form_class = forms.SetPasswordForm
    page_title = _("Set Password")
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.has_password():
            return HttpResponseBadRequest(
                "400 BAD REQUEST Password already set")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.user.set_password(form.cleaned_data['password'])
        self.request.user.save()
        update_session_auth_hash(self.request, self.request.user)
        messages.success(self.request, _("Password was set succesfully"))
        return super().form_valid(form)


class UserDisplayNamesView(ProtectedViewMixin, UpdateView):
    template_name = "users/set-names.html"
    form_class = forms.UserDisplayNamesForm
    page_title = _("My Profile")
    success_url = reverse_lazy("sa:dashboard")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _("Profile saved successfully."))
        return super().form_valid(form)
