from django.conf import settings
from django.db import models
from django_extensions.db.fields.json import JSONField
from . import consts

# from users.models import UserLogOperation, UserLog
from q13es.forms import get_pretty_answer


class Application(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    forms_filled = models.IntegerField(default=0, db_index=True)
    last_form_filled = models.DateTimeField(null=True, blank=True,
                                            db_index=True)


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='answers')
    q13e_slug = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    data = JSONField()

    class Meta:
        unique_together = (('user', 'q13e_slug'),)

    def __str__(self):
        return "%s: %s (%s)" % (self.user, self.q13e_slug, self.created_at)

    def get_pretty(self):
        form = consts.FORMS[self.q13e_slug]
        return dict(get_pretty_answer(form, self.data), answer=self)

#
#
# class Cohort(models.Model):
#     ordinal = models.IntegerField(unique=True)
#     code = models.CharField(max_length=10, unique=True)
#     title = models.CharField(max_length=200)
#     description = models.TextField(null=True, blank=True)
#
#     def __unicode__(self):
#         return self.title
#
#     class Meta:
#         ordering = ['ordinal']
#
#     @models.permalink
#     def get_absolute_url(self):
#         return "cohort", (self.code,)
#
#     def users_in_pipeline(self):
#         return self.users.filter(status__in=UserCohortStatus.PIPELINE)
#
#
# class UserCohortStatus(object):
#     INVITED = 1
#
#     UNAVAILABLE = 2
#
#     AVAILABLE = 10
#
#     INVITED_TO_INTERVIEW = 50
#
#     REJECTED = 99
#     ACCEPTED = 100
#     IN_OTHER_COHORT = 101
#
#     REGISTERED = 110
#     IN_PROCESS = 200
#     GRADUATED = 300
#
#     choices = (
#         (INVITED, _('Invited')),
#         (UNAVAILABLE, _('Unavailable')),
#         (AVAILABLE, _('Available')),
#         (INVITED_TO_INTERVIEW, _('Invited to interview')),
#
#         (REJECTED, _('Rejected')),
#         (ACCEPTED, _('Accepted')),
#         (IN_OTHER_COHORT, _('Accepted to another cohort')),
#
#         (REGISTERED, _('Registered')),
#         (IN_PROCESS, _('In process')),
#         (GRADUATED, _('Graduated')),
#     )
#
#     PIPELINE = [AVAILABLE, INVITED_TO_INTERVIEW, ACCEPTED, REGISTERED,
#                 IN_PROCESS, GRADUATED]
#     IGNORED = [INVITED, UNAVAILABLE, REJECTED, IN_OTHER_COHORT]
#
#
# class UserCohort(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="cohorts")
#     cohort = models.ForeignKey(Cohort, related_name="users")
#     status = models.IntegerField(choices=UserCohortStatus.choices)
#     statuses = UserCohortStatus
#
#     class Meta:
#         unique_together = (
#             ('user', 'cohort'),
#         )
#         ordering = ['cohort', 'status']
#
#
# class TagGroup(object):
#     NEGATIVE = -100
#     NEUTRAL = 0
#     BRONZE = 100
#     SILVER = 200
#     GOLD = 300
#
#     choices = (
#         (NEGATIVE, 'negative'),
#         (NEUTRAL, 'neutral'),
#         (BRONZE, 'bronze'),
#         (SILVER, 'silver'),
#         (GOLD, 'gold'),
#     )
#
#
# class Tag(models.Model):
#     name = models.CharField(max_length=100)
#     group = models.IntegerField(choices=TagGroup.choices,
#                                 default=TagGroup.NEUTRAL)
#
#     class Meta:
#         ordering = ['-group', 'name']
#
#     def __unicode__(self):
#         return self.name
#
#
# class UserTagManager(models.Manager):
#     def tag(self, user, tag, by):
#         with transaction.commit_on_success():
#             o, created = self.get_or_create(user=user, tag=tag, created_by=by)
#             if created:
#                 UserLog.objects.create(user=user, created_by=by,
#                                        content_object=tag,
#                                        operation=UserLogOperation.ADD)
#         return o
#
#     def untag(self, user, tag, by):
#         with transaction.commit_on_success():
#             try:
#                 o = self.get(user=user, tag=tag, created_by=by)
#                 o.delete()
#                 UserLog.objects.create(user=user, created_by=by,
#                                        content_object=tag,
#                                        operation=UserLogOperation.REMOVE)
#                 return True
#             except UserTag.DoesNotExist:
#                 return False
#
#
# class UserTag(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tags")
#     tag = models.ForeignKey(Tag, related_name='users')
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
#                                    related_name="tags_created")
#
#     objects = UserTagManager()
#
#     class Meta:
#         unique_together = (
#             ('user', 'tag', 'created_by'),
#         )
