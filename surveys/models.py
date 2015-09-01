import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields.json import JSONField
from hackita02.mail import send_html_mail

from q13es.forms import parse_form, get_pretty_answer
from hackita02.html import HTMLField
from users.models import generate_code

logger = logging.getLogger(__name__)


class Survey(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    email_subject = models.CharField(_('email subject'), max_length=250)
    email_content = HTMLField(_('email content'), null=True, blank=True)
    q13e = models.TextField()

    class Meta:
        verbose_name = _("survey")
        verbose_name_plural = _("surveys")

    def __str__(self):
        return self.email_subject

    def get_form_class(self):
        return parse_form(self.q13e)

    def add_user(self, user):
        return SurveyAnswer.objects.get_or_create(survey=self, user=user)

    def get_absolute_url(self):
        return reverse("surveys:detail", args=(self.pk,))


class SurveyAnswer(models.Model):
    survey = models.ForeignKey(Survey, related_name='answers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='survey_answers')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default=generate_code)
    answered_at = models.DateTimeField(null=True, blank=True)
    data = JSONField(null=True, blank=True)

    class Meta:
        unique_together = (
            ('survey', 'user'),
        )

    def __str__(self):
        return "%s: %s (%s)" % (self.survey, self.user, self.created_at)

    def get_pretty(self):
        dct = get_pretty_answer(self.survey.get_form_class(), self.data)
        dct['answer'] = self
        return dct

    def get_absolute_url(self):
        return reverse("surveys:answer", args=(self.slug,))

    def send(self, base_url=""):
        """ sends an email to user  """

        context = {'base_url': base_url, 'object': self}

        html_message = render_to_string("surveys/survey_email.html", context)

        logger.info("Sending survey (#%d) for survey #%d to user #%d at %s"
                    % (self.id, self.survey.id, self.user.id, self.user.email))

        send_html_mail(
            self.survey.email_subject,
            html_message,
            self.user.email,
        )

        return True
