from django.contrib import messages
from django.core.mail import mail_managers
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from events import forms
from events.models import EventInvitation, EventInvitationStatus, Event
from hackita02.base_views import TeamOnlyMixin
from users.models import PersonalInfo


class EventListView(TeamOnlyMixin, ListView):
    page_title = _("Events")
    model = Event


class EventDetailView(TeamOnlyMixin, DetailView):
    model = Event

    @property
    def page_title(self):
        return "{} | {}".format(self.object, _("Events"))


class EventContactsView(TeamOnlyMixin, DetailView):
    model = Event
    template_name = "events/event_contacts.html"

    def get_context_data(self, **kwargs):
        def f(invite):
            assert isinstance(invite, EventInvitation)
            declined = invite.status == EventInvitationStatus.DECLINED
            try:
                info = invite.user.personalinfo
                return (
                    declined, info.hebrew_first_name, info.hebrew_last_name)
            except PersonalInfo.DoesNotExist:
                return (declined, invite.user.email, "")

        d = super().get_context_data(**kwargs)
        qs = self.object.invitations.all()
        d['invites'] = sorted(qs, key=f)
        return d


class InvitationDetailView(DetailView):
    model = EventInvitation

    def post(self, request, *args, **kwargs):

        try:
            status = int(request.POST.get('status', '0'))
        except ValueError:
            status = 0
        if status not in [EventInvitationStatus.APPROVED,
                          EventInvitationStatus.DECLINED,
                          EventInvitationStatus.MAYBE]:
            return HttpResponseBadRequest("Bad status value")

        note = request.POST.get('note')

        o = self.get_object()

        if o.event.ends_at < timezone.now():
            messages.error(request, _("Event already finished."))

        else:
            if status != o.status or note != o.note:
                if o.registration_allowed():
                    o.status = status
                    o.note = note
                    o.save()
                    subject = u"%s: %s - %s" % (
                        o.user, o.get_status_display(), o.event)
                    message = u"%s (%s): %s - %s\n%s" % (o.user, o.user.email,
                                                         o.get_status_display(),
                                                         o.event,
                                                         o.note)
                    mail_managers(subject, message)
                    messages.success(request, _('Thank you!'))
                else:
                    messages.error(request, _('Registration already closed.'))
            else:
                messages.success(request, _('Thank you!'))

        return redirect(o)


class InvitationPreviewView(TeamOnlyMixin, DetailView):
    model = EventInvitation
    template_name = "emails/invitation.html"


class InvitationUpdateView(TeamOnlyMixin, UpdateView):
    model = EventInvitation
    form_class = forms.EventInvitationForm

    def form_valid(self, form):
        d = super().form_valid(form)
        messages.success(self.request, _("Invitation updated successfully"))
        return d

    def get_success_url(self):
        if 'from' in self.request.POST:
            return self.request.POST['from']
        return self.get_object().user.get_absolute_url()
