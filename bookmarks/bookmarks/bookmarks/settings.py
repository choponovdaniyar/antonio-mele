from pathlib import Path
import os

from environs import Env

from django.urls import reverse_lazy


env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('SECRET_KEY')

DEBUG = True

# для пакета 'sorl-thumbnail'
THUMBNAIL_DEBUG=True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [

    'account.apps.AccountConfig',
    'images.apps.ImagesConfig',
    'social_django',

    'django.contrib.admin',
    'django.contrib.auth',    
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'actions',

    'sorl.thumbnail',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookmarks.urls'

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
                'social_django.context_processors.backends', #social_django
            ],
        },
    },
]

WSGI_APPLICATION = 'bookmarks.wsgi.application'

# production/locale
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Системы аутентификации пользователя
AUTHENTICATION_BACKENDS = [  
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.vk.VKOAuth2', # vk social_django
    'social_core.backends.facebook.FacebookOAuth2', # facebook social_django
    'social_core.backends.twitter.TwitterOAuth', # twitter social_django
    'social_core.backends.google.GoogleOAuth2', # google social_django
]
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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/'
# locale
STATIC_DIR = os.path.join(BASE_DIR, 'static')
# production
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# locale
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = 'testing@example.com'

LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'



SITE_ID = 1 



# Если используется СУБД PostgreSQL для пакета social_django
SOCIAL_AUTH_POSTGRES_JSONFIELD = True

SOCIAL_AUTH_VK_OAUTH2_KEY = "8180316" # Vk App Id
SOCIAL_AUTH_VK_OAUTH2_SECRET = "otrvi9HSajU8T3XOScH7" # Vk App Key

SOCIAL_AUTH_FACEBOOK_KEY = "427403829238495" # Facebook App Key
SOCIAL_AUTH_FACEBOOK_SECRET = "186be46678a2f304cb67f41e407fe589" # Facebook App Secret

SOCIAL_AUTH_TWITTER_KEY = 'XXX' # Twitter Consumer Key
SOCIAL_AUTH_TWITTER_SECRET = "" # Twitter Consumer Secret

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'XXX' # Google Consumer Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'XXX' # Google Consumer Secret


# динамическое добавление get_absolute_url
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail', args=[u.username])
}

# redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0