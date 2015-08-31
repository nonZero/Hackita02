import logging

from django.contrib.auth.decorators import login_required
from django.core.mail import mail_managers
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone

from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView, \
    View

from django.utils.translation import ugettext_lazy as _

from . import forms, models
from django.views.generic.detail import SingleObjectMixin
from hackita02.base_views import UIMixin, PermissionMixin, ProtectedViewMixin

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
        form = forms.ProjectVoteForm(data, instance=o)
        form.fields['score'].widget.choices = form.fields[
                                                  'score'].widget.choices[1:]
        return form

    def get_comment_form(self, data=None):
        return forms.ProjectCommentForm(data)

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d['vote_form'] = self.get_vote_form()
        d['comment_form'] = self.get_comment_form()
        return d

    def handle_vote_form(self):
        form = self.get_vote_form(self.request.POST)
        if not form.is_valid():
            return False

        form.instance.user = self.request.user
        form.instance.project = self.object
        form.save()
        return True

    def handle_comment_form(self):
        form = self.get_comment_form(self.request.POST)
        if not form.is_valid():
            return False

        form.instance.user = self.request.user
        form.instance.project = self.object
        form.save()
        form.instance.new = True

        url = self.request.build_absolute_uri(form.instance.get_absolute_url())

        subject = "{}: {} -> {}".format(
            _("Comment posted"),
            self.request.user,
            self.object,
        )
        message = "{}\n\n{}\n{}\n\n{} ({})".format(
            url,
            form.instance.get_scope_display(),
            form.instance.content,
            self.request.user,
            self.request.user.email,
        )
        mail_managers(subject, message)

        response = render_to_string("projects/_project_comment.html",
                                    {'c': form.instance, },
                                    request=self.request)
        return response

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form_type = self.request.POST.get('type')

        if form_type == 'vote':
            result = self.handle_vote_form()
        elif form_type == 'comment':
            result = self.handle_comment_form()
        else:
            result = False

        return JsonResponse({'result': result}, safe=False,
                            status=200 if result else 400)


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


class ProjectCommentListView(PermissionMixin, UIMixin, ListView):
    permission_required = "projects.projectcomment_view"
    model = models.ProjectComment
    paginate_by = 50


class ProjectCommentUpdateView(PermissionMixin, UIMixin, UpdateView):
    permission_required = "projects.projectcomment_change"
    model = models.ProjectComment
    form_class = forms.ProjectCommentEditForm


class ProjectCommentMarkReviewedView(PermissionMixin, SingleObjectMixin, View):
    permission_required = "projects.projectcomment_change"
    model = models.ProjectComment

    def post(self, request, *args, **kwargs):
        o = self.get_object()
        o.is_reviewed = True
        o.reviewed_by = self.request.user
        o.reviewed_at = timezone.now()
        o.save()
        return JsonResponse({})
