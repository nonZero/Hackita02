from __future__ import unicode_literals

import floppyforms.__future__ as forms

from . import models


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = (
            'status',
        )


class ApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = models.ApplicationReview
        fields = (
            'programming_exp',
            'webdev_exp',
            'activism_level',
            'availability',
            'humanism_background',
            'comm_skills',
            'overall_impression',
            'comments',
        )
