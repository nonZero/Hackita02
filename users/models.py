from __future__ import unicode_literals

from authtools.models import AbstractNamedUser

# from django.utils.translation import ugettext_lazy as _


class User(AbstractNamedUser):
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'auth_user'
        ordering = (
            '-is_superuser',
            '-is_staff',
            '-last_login',
            'name',
        )

    def get_absolute_url(self):
        return "/users/%d/" % self.id


    def __unicode__(self):
        return self.name