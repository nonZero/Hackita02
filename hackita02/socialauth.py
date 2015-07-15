from pprint import pprint

from django.conf import settings
from django.core.mail import send_mail, mail_managers
from django.core.urlresolvers import reverse
from social.backends.email import EmailAuth
from social.exceptions import AuthMissingParameter, AuthException
from social.exceptions import InvalidEmail
from social.pipeline.partial import partial
from django.utils.translation import ugettext_lazy as _


def create_user(strategy, details, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    return {
        'is_new': True,
        'user': strategy.create_user(email=details['email'])
    }


def send_validation(strategy, backend, code):
    url = '{}?verification_code={}'.format(
        reverse('social:complete', args=(backend.name,)),
        code.code
    )
    url = strategy.request.build_absolute_uri(url)
    send_mail(_('Your Hackita 02 Login Link'), '{}:\n{}'.format(
        _("To login to Hackita 02, click here"),
        url), settings.EMAIL_FROM, [code.email])


def associate_by_email(backend, details, user=None, *args, **kwargs):
    """
    Associate current auth with a user with the same email address in the DB.

    This pipeline entry is not 100% secure unless you know that the providers
    enabled enforce email verification on their side, otherwise a user can
    attempt to take over another user account by using the same (not validated)
    email address on some provider.  This pipeline entry is disabled by
    default.
    """
    if backend.name == "email":
        return None

    email = details.get('email')
    if email:
        # Try to associate accounts registered with the same email address,
        # only if it's a single object. AuthException is raised if multiple
        # objects are returned.
        users = list(backend.strategy.storage.user.get_users_by_email(email))
        if len(users) == 0:
            return None
        elif len(users) > 1:
            raise AuthException(
                backend,
                'The given email address is associated with another account'
            )
        else:
            return {'user': users[0]}


def notify_managers(backend, details, user=None, *args, is_new=False,
                    **kwargs):
    if not is_new:
        return

    title = "New {} User: {}".format(backend.name, user.email)
    mail_managers(title, title)


@partial
def mail_validation(backend, details, is_new=False, *args, **kwargs):
    if backend.name != "email":
        return

    data = backend.strategy.request_data()
    if 'verification_code' in data:
        backend.strategy.session_pop('email_validation_address')
        if not backend.strategy.validate_email(details['email'],
                                               data['verification_code']):
            raise InvalidEmail(backend)
    else:
        backend.strategy.send_email_validation(backend, details['email'])
        backend.strategy.session_set('email_validation_address',
                                     details['email'])
        return backend.strategy.redirect(
            backend.strategy.setting('EMAIL_VALIDATION_URL')
        )


class HackitaEmailAuth(EmailAuth):
    PASSWORDLESS = True

    def complete(self, *args, **kwargs):
        try:
            return self.auth_complete(*args, **kwargs)
        except AuthMissingParameter:
            return None


def debug(response, details, *args, pipeline_index, **kwargs):
    print(str(pipeline_index).center(20, "="))
    pprint(response)
    print('-' * 80)
    pprint(details)
    print('-' * 80)
    pprint(args)
    print('-' * 80)
    pprint(kwargs)
    print('=' * 80)
