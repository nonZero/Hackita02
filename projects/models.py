from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from projects.drive import retrieve_doc_content


class Project(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(_('title'), max_length=250, blank=False)
    summary = models.TextField(_('summary'))
    doc_id = models.CharField(_('title'), max_length=250, blank=False)
    content_text = models.TextField(_('content text'))
    content_html = models.TextField(_('content html'))
    refreshed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:detail", args=(self.id,))

    def retrieve_content(self, title=False):
        d = retrieve_doc_content(self.doc_id)
        self.content_text = d['text']
        self.content_html = d['html']
        if title:
            self.title = d['title']
        return d

