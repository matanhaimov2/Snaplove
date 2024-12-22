"""
Django settings for snaplove project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Secret key and other sensitive configurations
SECRET_KEY = config('SECRET_KEY')
# - If True => local db applyed, If False - server db (AIVEN) applyed
USE_LOCAL_DB = config('USE_LOCAL_DB', default=False, cast=bool)
# - If True => local cache applyed, If False - server cache (Redis Cloud) applyed
USE_LOCAL_CACHE = config('USE_LOCAL_CACHE', default=False, cast=bool)
NEON_PASSWORD = config('NEON_PASSWORD')
REDIS_PASSWORD = config('REDIS_PASSWORD')

# CORS settings from .env
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000,http://localhost').split(',')
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='http://localhost:3000,http://localhost').split(',')

# Allow hosts from environment variable
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    'daphne' , 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Modules
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_resized',
    'channels', 

    # Apps
    'users',
    'profiles',
    'interactions'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ASGI_APPLICATION = 'snaplove.asgi.application'

if USE_LOCAL_CACHE:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        },
    }
else:
    # Redis Cloud
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [
                    f"redis://:{REDIS_PASSWORD}@redis-11596.c6.eu-west-1-1.ec2.redns.redis-cloud.com:11596/0"
                ],
            },
        },
    }

ROOT_URLCONF = 'snaplove.urls'

# Allow all credentials for CORS
CORS_ALLOW_CREDENTIALS = True

# CSRF and session security settings
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTP_ONLY = True
CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"

# Expose CSRF Token and Content-Type header for cross-origin requests
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]

CSRF_TRUSTED_ORIGINS = [
    *CORS_ALLOWED_ORIGINS # Use the value from the .env file
]

CORS_ALLOWED_ORIGINS = [
    *CSRF_TRUSTED_ORIGINS # Use the value from the .env file
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.authenticate.CustomAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

    # custom
    'AUTH_COOKIE': 'access',
    # Cookie name. Enables cookies if value is set.
    'AUTH_COOKIE_REFRESH': 'refresh',
    # A string like "example.com", or None for standard domain cookie.
    'AUTH_COOKIE_DOMAIN': None,
    # Whether the auth cookies should be secure (https:// only).
    'AUTH_COOKIE_SECURE': True, 
    # Http only cookie flag.It's not fetch by javascript.
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_PATH': '/',        # The path of the auth cookie.
    # Whether to set the flag restricting cookie leaks on cross-site requests. This can be 'Lax', 'Strict', or None to disable the flag.
    'AUTH_COOKIE_SAMESITE': "None", # TODO: Modify to Lax
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'snaplove.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if USE_LOCAL_DB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql', # Using PostgreSQL as the database engine
            'NAME': 'snaplove-db', # The name of the local PostgreSQL database
            'USER': 'postgres', # Local database username (default for PostgreSQL)
            'PASSWORD': 'Matan2004', # Local database password
            'HOST': '127.0.0.1', # The host address for the local database (127.0.0.1 means localhost)
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql', # Using PostgreSQL as the database engine
            'NAME': 'pg-snaplove', # The name of the remote PostgreSQL database (on the server)
            'USER': 'pg-snaplove_owner', # The username for the server's PostgreSQL database
            'PASSWORD': NEON_PASSWORD, # Fetch the PostgreSQL password from the environment
            'HOST': 'ep-still-king-a2dzq3tq.eu-central-1.aws.neon.tech', # The host address of the PostgreSQL server
            'PORT': '5432', # The port for connecting to the PostgreSQL server (default port is usually 5432)
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = 'media/'
MEDIA_ROOT = 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTH_USER_MODEL = User