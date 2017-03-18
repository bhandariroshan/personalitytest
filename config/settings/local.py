# -*- coding: utf-8 -*-
"""
Local settings

- Run in Debug mode

- Use console backend for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""

import socket
import os
from .base import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

ALLOWED_HOSTS = ['139.59.236.7', 'localhost', '127.0.0.1']

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='Jhbp(o7@=Y%C:])]ST?T)ozfjbbz!.p#ajI(HI<0^z<8Vn2W+T')

# Mail settings
# ------------------------------------------------------------------------------

EMAIL_PORT = 1025

EMAIL_HOST = 'localhost'
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')


# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INSTALLED_APPS += ['debug_toolbar', ]

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]
# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1']

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions', ]

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------


ALLOWED_HOSTS = ['139.59.236.7', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS += [
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    # 'django.contrib.staticfiles',
    # 'django.contrib.sites',
    'rest_framework',
    # allauth
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.twitter',
    'djcelery',
    # # local apps
    'mainapp',
    'action',
]

MIDDLEWARE += [
    # 'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.CacheMiddleware',
]