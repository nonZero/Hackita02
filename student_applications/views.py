# coding: utf-8

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_managers
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import transaction
from django.shortcuts import redirect
from django.template import loader
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView

from . import models
from student_applications.consts import get_user_progress, FORMS, \
    get_user_next_form, FORM_NAMES
from users.base_views import ProtectedMixin, StaffOnlyMixin
from users.forms import PersonalInfoForm
from users.models import PersonalInfo

logger = logging.getLogger(__name__)


class UserViewMixin(ProtectedMixin):
    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)

        d['filled_count'], d['total_count'] = get_user_progress(
            self.request.user)
        d['progress'] = int(100 * (d['filled_count'] + 1) /
                            (d['total_count'] + 1))

        return d


class Dashboard(UserViewMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d['registered'] = get_user_next_form(self.request.user) is None
        d['needs_personal_details'] = not hasattr(self.request.user,
                                                  'personalinfo')
        return d


class PersonalDetailsView(UserViewMixin, CreateView):
    model = PersonalInfo
    form_class = PersonalInfoForm
    success_url = reverse_lazy("sa:dashboard")

    def dispatch(self, request, *args, **kwargs):
        """Prevent filling personal information twice"""
        if hasattr(self.request.user, 'personalinfo'):
            return redirect(reverse("sa:dashboard"))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        with transaction.atomic():
            form.instance.user = user
            dirty = False
            if not user.english_display_name:
                user.hebrew_display_name = "{} {}".format(
                    form.cleaned_data['hebrew_first_name'].strip(),
                    form.cleaned_data['hebrew_last_name'].strip(),
                )
                dirty = True
            if not user.english_display_name:
                user.english_display_name = "{} {}".format(
                    form.cleaned_data['english_first_name'].strip().title(),
                    form.cleaned_data['english_last_name'].strip().title(),
                )
                dirty = True
            if dirty:
                user.save()
            resp = super().form_valid(form)

        messages.info(self.request, _("Personal details saved successfully."))

        return resp


class ReviewView(UserViewMixin, TemplateView):
    template_name = 'review.html'

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)

        d['registered'] = get_user_next_form(self.request.user) is None

        # if d['registered']:
        #     d['answers'] = get_user_pretty_answers(self.request.user)

        return d


class RegisterView(UserViewMixin, FormView):
    template_name = 'register.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        form = self.get_form_class()
        if form is None:
            return redirect('sa:dashboard')

        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        form_name = get_user_next_form(self.request.user)
        if not form_name:
            return None

        return FORMS[form_name]

    def form_valid(self, form):
        u = self.request.user
        data = form.cleaned_data
        form_name = get_user_next_form(u)

        logger.info("User %s filled %s" % (u, form_name))

        a = models.Answer.objects.create(user=u, q13e_slug=form_name,
                                         data=data)

        try:
            app = u.application
        except models.Application.DoesNotExist:
            app = models.Application(user=u)
        app.forms_filled = u.answers.count()
        app.last_form_filled = a.created_at
        app.save()

        if get_user_next_form(u) is None:
            messages.success(self.request,
                             _("Registration completed! Thank you very much!"))
            text, html = self.get_summary_email(u)
            mail_managers(_("User registered: %s") % u.email, text,
                          html_message=html)
            return redirect('sa:dashboard')

        messages.success(self.request, _("'%s' was saved.") % form.form_title)

        return redirect(reverse('sa:register'))

    def get_summary_email(self, u):
        url = self.request.build_absolute_uri(reverse('sa:app_detail',
                                                      args=(u.application.id,)))
        html = loader.render_to_string(
            "student_applications/application_summary_email.html", {
                'u': u,
                'url': url
            }, request=self.request)
        return url, html

    def form_invalid(self, form):
        messages.warning(self.request,
                         _("Problems detected in form. "
                           "Please fix your errors and try again."))
        return FormView.form_invalid(self, form)


class AllFormsView(TemplateView, ProtectedMixin):
    template_name = 'all-forms.html'

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d['forms'] = [(k, FORMS[k]) for k in FORM_NAMES]
        return d


class ApplicationListView(StaffOnlyMixin, ListView):
    model = models.Application
    ordering = ('-forms_filled', '-last_form_filled')


class ApplicationDetailView(StaffOnlyMixin, DetailView):
    model = models.Application

# class UserCohortUpdateView(StaffOnlyMixin, InlineFormSetView):
#     model = HackitaUser
#     inline_model = UserCohort
#     template_name = 'student_applications/usercohort_formset.html'
#     extra = 0
#     can_delete = False
#     fields = ('status',)
#
#     def get_success_url(self):
#         if 'from' in self.request.POST:
#             return self.request.POST['from']
#         return self.get_object().get_absolute_url()
#
#
# class CohortListView(StaffOnlyMixin, ListView):
#     model = Cohort
#
#
# class CohortDetailView(StaffOnlyMixin, UsersOperationsMixin, DetailView):
#     model = Cohort
#     slug_field = 'code'
#
#     def get_context_data(self, **kwargs):
#         d = super(CohortDetailView, self).get_context_data(**kwargs)
#         d['statuses'] = UserCohortStatus.choices
#         return d
#
#     def post(self, request, *args, **kwargs):
#
#         cohort = self.get_object()
#
#         if request.POST.get('status'):
#             status = int(request.POST.get('status'))
#             for uid in self.get_user_ids():
#                 user = HackitaUser.objects.get(pk=uid)
#                 uc = UserCohort.objects.get(user=user, cohort=cohort)
#                 if uc.status != status:
#                     uc.status = status
#                     uc.save()
#                     messages.success(request, u"%s: %s" %
#                                               (user, uc.get_status_display()))
#                     # fall through.
#
#         # Send surveys
#         if request.POST.get('survey'):
#             return redirect(self.send_survey(request))
#
#         # Send event invitations
#         if request.POST.get('event'):
#             return redirect(self.send_invites(request))
#
#         return redirect(cohort)
