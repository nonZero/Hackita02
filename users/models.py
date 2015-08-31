from __future__ import unicode_literals
import random

from authtools.models import AbstractNamedUser, AbstractEmailUser
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django.contrib.auth.models import BaseUserManager
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models

from django.utils.translation import ugettext_lazy as _
from hackita02 import settings


class UserManager(BaseUserManager):
    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the address by lowercasing it.
        """
        return email.lower()

    def create_user(self, email, password=None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractEmailUser):
    hebrew_display_name = models.CharField(_("display name (Hebrew)"),
                                           max_length=200, null=True,
                                           blank=True)
    english_display_name = models.CharField(_("display name (English)"),
                                            max_length=200, null=True,
                                            blank=True)

    objects = UserManager()

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

    def has_password(self):
        return self.password and not self.password.startswith(
            UNUSABLE_PASSWORD_PREFIX)

    def __str__(self):
        if self.hebrew_display_name:
            return self.hebrew_display_name
        try:
            if self.personalinfo.hebrew_first_name:
                return "{} {}".format(
                    self.personalinfo.hebrew_first_name,
                    self.personalinfo.hebrew_last_name,
                )
        except PersonalInfo.DoesNotExist:
            pass

        return "{} #{}".format(_("Anonymouse User"), self.id)


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

    class Meta:
        verbose_name = _("pesronal info")
        verbose_name_plural = _("pesronal infos")


def generate_code(length=32):
    return ''.join(
        [random.choice(
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
         for i in range(length)])


class CodeManager(models.Manager):
    def generate(self, email):
        return self.create(email=email.lower(), code=generate_code())


class Code(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    code = models.CharField(max_length=32, unique=True)
    verified = models.BooleanField(default=False)

    objects = CodeManager()

    def send_validation(self, host_url):
        url = host_url + reverse('users:validate', args=(self.code,), )
        send_mail(
            _('Your Hackita 02 Login Link'),
            '{}:\n{}'.format(_("To login to Hackita 02, click here"), url),
            settings.EMAIL_FROM, [self.email]
        )
