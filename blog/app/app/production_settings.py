from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEBUG = False

ALLOWED_HOSTS = [ 'domain or ip']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgesql',
        'NAME': 'postgres',
    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')