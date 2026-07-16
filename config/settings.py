"""
Django settings for Article 159 landing project.
"""

from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-dev-only-change-me-article-159-landing',
)

# Render sets RENDER=true automatically
ON_RENDER = os.getenv('RENDER', '').lower() in ('1', 'true', 'yes')

DEBUG = os.getenv('DEBUG', 'False' if ON_RENDER else 'True').lower() in ('1', 'true', 'yes')

_default_hosts = '127.0.0.1,localhost'
if ON_RENDER:
    _default_hosts = (
        '127.0.0.1,localhost,.onrender.com,'
        'advokat-allazov-159.onrender.com'
    )

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv('ALLOWED_HOSTS', _default_hosts).split(',')
    if host.strip()
]

# Always allow Render host even if env vars were forgotten
for _host in ('.onrender.com', 'advokat-allazov-159.onrender.com'):
    if _host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_host)

_default_csrf = (
    'https://*.onrender.com,https://advokat-allazov-159.onrender.com'
    if ON_RENDER
    else ''
)

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv('CSRF_TRUSTED_ORIGINS', _default_csrf).split(',')
    if origin.strip()
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'landing.apps.LandingConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'landing.context_processors.site_contacts',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Site contacts (override via .env)
SITE_PHONE = os.getenv('SITE_PHONE', '+7 (926) 122-31-33')
SITE_PHONE_RAW = os.getenv('SITE_PHONE_RAW', '+79261223133')
SITE_WHATSAPP = os.getenv('SITE_WHATSAPP', '79261223133')
SITE_TELEGRAM = os.getenv('SITE_TELEGRAM', 'https://t.me/advokatallazov')
SITE_EMAIL = os.getenv('SITE_EMAIL', 'Allazov009@mail.ru')
SITE_LAWYER_NAME = os.getenv('SITE_LAWYER_NAME', 'Аллазов Мансур Анварович')
SITE_LAWYER_TITLE = os.getenv('SITE_LAWYER_TITLE', 'Адвокат')

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
