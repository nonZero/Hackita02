from __future__ import unicode_literals

from authtools.models import AbstractNamedUser, AbstractEmailUser
from django.db import models

from django.utils.translation import ugettext_lazy as _


class User(AbstractEmailUser):
    hebrew_display_name = models.CharField(_("display name (Hebrew)"),
                                           max_length=200, null=True,
                                           blank=True)
    english_display_name = models.CharField(_("display name (English)"),
                                           max_length=200, null=True,
                                           blank=True)

    class Meta:
        db_table = 'auth_user'
        ordering = (
            '-is_superuser',
            '-is_staff',
            '-last_login',
            'hebrew_display_name',
            'email',
        )

    def get_absolute_url(self):
        return "/users/%d/" % self.id

    def __unicode__(self):
        return self.email


class PersonalInfo(models.Model):
    user = models.OneToOneField(User)
    hebrew_first_name = models.CharField(_("first name (Hebrew)"),
                                         max_length=200)
    hebrew_last_name = models.CharField(_("last name (Hebrew)"),
                                        max_length=200)
    english_first_name = models.CharField(_("first name (English)"),
                                          max_length=200)
    english_last_name = models.CharField(_("last name (English)"),
                                         max_length=200)

    FEMALE = 1
    MALE = 2
    NA = 3
    GENDER_CHOICES = (
        (FEMALE, _("female")),
        (MALE, _("male")),
        (NA, _("prefer not to answer")),
    )
    gender = models.IntegerField(
        _("gender"), choices=GENDER_CHOICES, default=NA,
        help_text=_("we would like to create a diverse group."))

    main_phone = models.CharField(_("main phone number"), max_length=50)
    alt_phone = models.CharField(_("alternate phone number"), max_length=50,
                                 null=True, blank=True)
    city = models.CharField(_("city"), max_length=200, null=True, blank=True)
    address = models.TextField(_("address"), null=True, blank=True,
                               help_text=_("street and number"))

    skype_username = models.CharField(
        _("skype username"), max_length=100, null=True, blank=True,
        help_text=_("optional, for conducting a video interview."))
