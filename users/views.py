from email.utils import parseaddr

import authtools.views
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_managers
from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponseBadRequest, HttpResponse, \
    JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView, View, UpdateView, \
    DetailView, ListView
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import SingleObjectMixin

from . import forms
from . import models
from hackita02.base_views import ProtectedViewMixin, PermissionMixin
from hackita02.mail import send_html_mail


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


class UserListView(PermissionMixin, ListView):
    permission_required = "users.view_user"
    model = models.User


class UserDetailView(PermissionMixin, DetailView):
    permission_required = "users.view_user"
    model = models.User
    context_object_name = 'theuser'

    def get_note_form(self, data=None):
        return forms.UserNoteForm(data)

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d['note_form'] = self.get_note_form()
        return d

    def get_base_url(self):
        return self.request.build_absolute_uri('/')[:-1]

    def handle_note_form(self):
        form = self.get_note_form(self.request.POST)
        if not form.is_valid():
            return False

        note = form.instance
        assert isinstance(note, models.UserNote)
        note.user = self.object
        note.author = self.request.user
        form.save()

        models.UserLog.objects.create(user=self.object,
                                      created_by=self.request.user,
                                      content_object=note,
                                      operation=models.UserLogOperation.ADD)

        send_to_user = (form.cleaned_data['visible_to_user'] and
                        form.cleaned_data['send_to_user'])

        self.send_note_to_managers(note, send_to_user)

        if send_to_user:
            self.send_note_to_user(note)

        response = render_to_string("users/_user_note.html",
                                    {'note': note},
                                    request=self.request)
        return response

    def send_note_to_managers(self, note, sent_to_user):
        subject = "{} {} {} {}".format(
            _("User note posted to"),
            self.object,
            _("By"),
            self.request.user.real_name_or_email(),
        )
        url = note.get_absolute_url()
        html_message = render_to_string("users/usernote_email.html", {
            'base_url': self.get_base_url(),
            'managers': True,
            'sent_to_user': sent_to_user,
            'title': subject,
            'note': note,
            'url': url,
        }, request=self.request)
        mail_managers(subject, '', html_message=html_message)

    def send_note_to_user(self, note):
        subject = "{} {}".format(
            _("Hackita02: New note from"),
            self.request.user,
        )
        url = reverse("sa:dashboard")
        html_message = render_to_string("users/usernote_email.html", {
            'base_url': self.get_base_url(),
            'title': subject,
            'note': note,
            'url': url,
        }, request=self.request)
        send_html_mail(subject, html_message, note.user.email)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        result = self.handle_note_form()

        return JsonResponse({'result': result}, safe=False,
                            status=200 if result else 400)


class UserTagsEditView(PermissionMixin, ProtectedViewMixin, SingleObjectMixin,
                       FormView):
    permission_required = "users.change_user"
    form_class = forms.TagsForm
    template_name = "users/user_tags.html"
    model = models.User

    def get_success_url(self):
        return self.object.get_absolute_url()

    def pre_dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().pre_dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {'tags': [ut.tag for ut in self.object.tags.all()]}

    def form_valid(self, form):
        user = self.object
        tags = set(form.cleaned_data['tags'])
        current = set([ut.tag for ut in user.tags.all()])
        for tag in tags - current:
            models.UserTag.objects.tag(user, tag, self.request.user)
        for tag in current - tags:
            models.UserTag.objects.untag(user, tag, self.request.user)

        return super().form_valid(form)


class AllEmailsView(PermissionMixin, View):
    permission_required = "users.view_user"

    def get(self, request, *args, **kwargs):
        text = "\n".join(x.email for x in models.User.objects.all())
        return HttpResponse(text, content_type='text/plain')
