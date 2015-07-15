# encoding: utf-8
from __future__ import print_function, unicode_literals

DEBUG = True
TEMPLATE_DEBUG = True
EXPLORE_USE_BUILD = False

SECRET_KEY = '{{secret_key}}'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

SHAPEFILES_PATH = "C:\\users\\udi\\from_npa\\shp"
INSTANCE_NAME = 'פיתוח'

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     },
#     'obs': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     },
# }
#
