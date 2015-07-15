_user = '{{webuser}}'
_host = '{{host}}'

ALLOWED_HOSTS = [_host]
FROM_EMAIL = "Hackita 02 <noreply@%s>   " % _host
DEFAULT_FROM_EMAIL = FROM_EMAIL
EMAIL_SUBJECT_PREFIX = '[%s] ' % _user.upper()

ADMINS = (
    ('{{user}}', '{{user}}@localhost'),
)

MANAGERS = ADMINS

SECRET_KEY = '{{secret_key}}'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': _user,
        'USER': _user,
        'PASSWORD': _user,
        'HOST': 'localhost',
        'PORT': '',
    },
}

GDRIVE_API_KEY = ''

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

GOOGLE_ANALYTICS_ID = 'UA-44855644-2'
