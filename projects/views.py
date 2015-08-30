import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from django.utils.translation import ugettext_lazy as _

from . import forms, models
from hackita02.base_views import UIMixin, PermissionMixin

logger = logging.getLogger(__name__)


class ProjectListView(UIMixin, ListView):
    name = 'projects'
    model = models.Project

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        published = self.get_queryset().published().random()
        if self.request.user.is_authenticated():
            for proj in published:
                proj.vote = proj.votes.filter(
                    user=self.request.user,
                ).first()
        d['published'] = published
        return d


class ProjectDetailView(UIMixin, DetailView):
    name = 'projects'
    model = models.Project

    def get_vote_form(self, data=None):
        if not self.request.user.is_authenticated():
            return None
        o = models.ProjectVote.objects.filter(
            project=self.object,
            user=self.request.user
        ).first()
        form = forms.VoteForm(data, instance=o)
        form.fields['score'].widget.choices = form.fields[
                                                  'score'].widget.choices[1:]
        return form

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d['vote_form'] = self.get_vote_form()
        return d

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_vote_form(self.request.POST)
        if not form.is_valid():
            return JsonResponse({'status': False}, safe=False, status=400)

        form.instance.user = self.request.user
        form.instance.project = self.object
        form.save()
        return JsonResponse({'status': True}, safe=False)


class ProjectCreateView(PermissionMixin, UIMixin, CreateView):
    name = 'projects'
    permission_required = "projects.project_create"
    model = models.Project
    form_class = forms.NewProjectForm

    def get_success_url(self):
        return self.object.get_update_url()

    def form_valid(self, form):
        try:
            form.instance.retrieve_content(title=True)
        except:
            raise
        form.instance.created_by = self.request.user
        form.instance.summary = _("EDIT ME")
        return super(ProjectCreateView, self).form_valid(form)


class ProjectUpdateView(PermissionMixin, UIMixin, UpdateView):
    permission_required = "projects.project_change"
    model = models.Project
    form_class = forms.UpdateProjectForm
