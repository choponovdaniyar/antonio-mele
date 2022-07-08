from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': "postgres",
        'PASSWORD': "qazwsx_00"
    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
