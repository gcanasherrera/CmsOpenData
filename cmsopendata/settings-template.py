"""
Django settings for cmsopendata project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9n)h#ax2!&64&q&345aklw542q4rnq5@&bt(2l*ery3$tybvio@6wedw!0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True 

#DEBUG = False 
#TEMPLATE_DEBUG = False

#ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'cmsopendata.ifca.es']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # OpenAccess
    'openaccess',
    # AUTH stuff
    'allauth',
    'allauth.account',
    # Required by auth stuff
    'django.contrib.sites',
    #'allauth.socialaccount',
    #'allauth.socialaccount.providers.google',
    'bootstrap_toolkit',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cmsopendata.urls'

WSGI_APPLICATION = 'cmsopendata.wsgi.application'


# enol: settings for django-allauth
SITE_ID = 1

TEMPLATE_CONTEXT_PROCESSORS = (
    # Required by allauth template tags
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    # allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = None

LOGIN_REDIRECT_URL = "/Analysis"

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


# Our stuff
OPENACCESS_ANALYSIS_SSH_HOST='xx.xx.xx.xx'
OPENACCESS_ANALYSIS_SSH_KEY='/home/ubuntu/id_rsa'
# default values
#OPENACCESS_ANALYSIS_SSH_PORT = 22
#OPENACCESS_ANALYSIS_SSH_USER = 'root'
#OPENACCESS_ANALYSIS_SSH_CMD = 'create_user'

# GateOne conf
OPENACCESS_GATEONE_SECRET = 'SOME SECRET'
OPENACCESS_GATEONE_KEY= 'SOME KEY'
OPENACCESS_GATEONE_PROFILE_DIR = '/var/gateone/user_profiles'
OPENACCESS_GATEONE_URL = 'https://cmsopendata.ifca.es/gateone'

STATIC_ROOT="/var/www/cmsopendata/static/"
STATIC_URL="/static/"
