import logging

from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.utils.translation import ugettext_lazy as _

from . import forms, models

from hackita02.base_views import UIMixin

logger = logging.getLogger(__name__)


class ProjectListView(UIMixin, ListView):
    model = models.Project


class ProjectDetailView(UIMixin, DetailView):
    model = models.Project


class ProjectCreateView(UIMixin, CreateView):
    model = models.Project
    form_class = forms.NewProjectForm

    def form_valid(self, form):
        try:
            form.instance.retrieve_content(title=True)
        except:
            raise
        form.instance.created_by = self.request.user
        form.instance.summary = _("EDIT ME")
        return super(ProjectCreateView, self).form_valid(form)


class ProjectUpdateView(UIMixin, UpdateView):
    model = models.Project
    form_class = forms.UpdateProjectForm
