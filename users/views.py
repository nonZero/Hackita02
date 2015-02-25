from __future__ import unicode_literals

from authtools.views import LoginView

from users.forms import CustomAuthenticationForm


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
