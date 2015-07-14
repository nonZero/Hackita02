import authtools.views
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

from . import forms


class LoginView(authtools.views.LoginView):
    template_name = "users/login.html"
    form_class = forms.LoginForm


class LogoutView(authtools.views.LogoutView):
    url = reverse_lazy(settings.LOGIN_URL)
