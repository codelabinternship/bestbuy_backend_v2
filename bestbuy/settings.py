"""
Production settings for zeinedtech project to use on Render with AWS S3.
"""

import os
import dj_database_url
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent / '.env.production'
load_dotenv(dotenv_path=env_path)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-change-me')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,.onrender.com').split(',')




# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')

# Print AWS configuration for debugging (remove in production)
if DEBUG:
    print("AWS Configuration:")
    print(f"Access Key ID: {'*' * 16 if AWS_ACCESS_KEY_ID else 'Not set'}")
    print(f"Secret Access Key: {'*' * 16 if AWS_SECRET_ACCESS_KEY else 'Not set'}")
    print(f"Bucket Name: {AWS_STORAGE_BUCKET_NAME or 'Not set'}")
    print(f"Region Name: {AWS_S3_REGION_NAME or 'Not set'}")
    print(f"Custom Domain: {AWS_S3_CUSTOM_DOMAIN or 'Not set'}")

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'media'






# Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'bestbuy_app',
    'telegram_bot',
    'corsheaders',
    'whitenoise.runserver_nostatic',
    #'storages',
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']
CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization', 'content-type',
    'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with',
]
#CORS_ALLOWED_ORIGINS = [
 #   "https://Bestbuy.uz",
  #  "https://Best-buy.uz",
   # "https://Bestbuy-admin.onrender.com",
    #"https://Best-buy-server.onrender.com",
#]

ROOT_URLCONF = 'bestbuy.urls'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    )
}

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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



SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'LOGIN_URL': None,
    'LOGOUT_URL': None,
    'SECURE_SCHEMA': 'https',
}








WSGI_APPLICATION = 'bestbuy.wsgi.application'

# # Database
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
            'NAME': 'bestbuy_db_ly3w',
            'USER': 'postgres_user',
            'PASSWORD': 'yTOGzwe9O6W4AkuDNYhRIVcCmRofHMsT',
            'HOST': 'dpg-d1d6o8be5dus73b25jf0-a',
            'PORT': '5432',
        }
    }


CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']



# DATABASES = {
#     'default':{
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'bestt',
#         'USER': 'postgres',
#         'PASSWORD': '8888',
#         'HOST': 'localhost',
#         'PORT': '5432'
#     }
# }

AUTH_USER_MODEL = 'bestbuy_app.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# I18N
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.environ.get('TIME_ZONE', 'Asia/Tashkent')
USE_I18N = True
USE_TZ = False

# Static
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MEDIA — S3 yoki local
#USE_S3 = os.getenv('USE_S3', 'False') == 'True'

#if USE_S3:
    #DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    #AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    #AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    #AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    #AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'eu-north-1')
    #AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN', f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com')
    #AWS_S3_FILE_OVERWRITE = False
    #AWS_DEFAULT_ACL = None
    #AWS_QUERYSTRING_AUTH = False
    #MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
#else:
    #DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    #MEDIA_URL = '/media/'
    #MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


#MEDIA_URL = '/media/'
#MEDIA_ROOT = BASE_DIR/'media'


#
# # AWS SETTINGS
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
#
# # STATIC
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{os.environ.get('STATIC_LOCATION', 'static')}/"
#
# # MEDIA
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{os.environ.get('MEDIA_LOCATION', 'media')}/"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')







# JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=3),
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Telegram
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# try:
#     from .settings_local import *
# except ImportError:
#     pass

