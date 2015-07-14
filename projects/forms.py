from django.utils.translation import ugettext_lazy as _
import floppyforms.__future__ as forms
from . import models
from projects.drive import id_from_url


class GoogleDocURLField(forms.URLField):
    def clean(self, value):
        v = super(GoogleDocURLField, self).clean(value)
        return id_from_url(v)


class NewProjectForm(forms.ModelForm):
    doc_id = GoogleDocURLField(label=_("google doc url"))

    class Meta:
        model = models.Project
        fields = (
            'doc_id',
        )

class UpdateProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = (
            'title',
            'summary',
        )
