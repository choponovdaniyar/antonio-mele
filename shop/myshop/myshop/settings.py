from pathlib import Path

from .cart_settings import *
from .celery_settings import *


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-01160%!ji2^(+qh&^62jl0@hxwg_neziwo2vv_pfi)wa-+v#18'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'shop.apps.ShopConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'payment.apps.PaymentConfig',
    'coupons.apps.CouponsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # корзина
    'django.contrib.sessions.middleware.SessionMiddleware',

    # локализация / интернациализация
    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                # корзина
                'cart.context_processor.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'myshop.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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




from django.utils.translation import gettext_lazy

# интернационализация
LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('en', gettext_lazy('English')),
    ('es', gettext_lazy('Spanish')),
)

LOCALE_PATH = [
    BASE_DIR / 'locale/',
]

TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# STATIC_ROOT = BASE_DIR / 'static/' # production
STATIC_URL = 'static/'
STATICFILES_DIRS = [ # local
    BASE_DIR / 'static',
]

MEDIA_URL = ''
MEDIA_ROOT =  BASE_DIR / 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# отправка сообщения на кансоль
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # дев
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # продакш


# Настройки Braintree / платежная система
# https://developers.braintreepayments.com/start/go-live/python инструкция для продакшна

from braintree import Configuration, Environment


BRAINTREE_MERCHANT_ID = '3zs832cfrtkb5rxn' # ID продавца.
BRAINTREE_PUBLIC_KEY = 'qbd75j9gt47fdwmm' # Публичный ключ.
BRAINTREE_PRIVATE_KEY = '1528473374dbb7c25508f4b8ae683fdc' # Секретный ключ

Configuration.configure(
    Environment.Sandbox, # 'Environment.Production' ДЛЯ продакшна
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY,
)



import sys
print(sys.path)