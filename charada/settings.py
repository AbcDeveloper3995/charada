
import os
import socket
from pathlib import Path

# CONFIGURACIONES COMUNES
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-s)o8(#&86hog&%svx#%@4gy667xl-=knv#bs00is425a)_mn_1'

DEBUG = True

ALLOWED_HOSTS = ['*']

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'apps.charada',
    'apps.usuario'
]

THRID_APPS = [
    'rest_framework',
    'pwa',
    'whitenoise.runserver_nostatic',
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THRID_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crum.CurrentRequestUserMiddleware'
]

ROOT_URLCONF = 'charada.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'charada.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'es'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

# LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/charada/home/'
LOGOUT_REDIRECT_URL = '/login/'

AUTH_USER_MODEL = 'usuario.Usuario'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PWA_APP_NAME = "Fhurer"
PWA_APP_DESCRIPTION = 'Proyecto'
PWA_APP_THEME_COLOR = '#3477f5'
PWA_APP_BACKGROUND_COLOR = '#6699f7'
PWA_APP_ICONS = [
    {
        "src": "/static/propios/img/logopwa.png",
        "sizes": "160x160"
    }
]

# CONFIGURACIONES LOCAL
if socket.gethostname() == 'DESKTOP-LVC68NK':
    DEBUG = TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': '127.0.0.1',
            'PORT': '5433',
        }
    }

    STATIC_URL = 'static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static")
    ]

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_TZ = True

# CONFIGURACIONES PRODUCCION
else:
    DEBUG = TEMPLATE_DEBUG = False
    ALLOWED_HOSTS = ['*']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': '127.0.0.1',
            'PORT': '5433',
        }
    }

    STATIC_URL = '/static/'

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static")
    ]
    STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')