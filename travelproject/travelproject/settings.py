"""
Django settings for travelproject project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%wdcnb&un5*0u9%p2uzp56ekd9nqjv_pk05depntr$5zk#iyor'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','127.0.0.1','travelagencyou.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'travelapp.apps.TravelappConfig',
    'ckeditor',
    'ckeditor_uploader',
    'corsheaders',
    # 'cloudinary_storage',
    'cloudinary',
    'rest_framework',
    'drf_yasg',
    'debug_toolbar',
    'oauth2_provider',
]

AUTH_USER_MODEL = 'travelapp.User'
CKEDITOR_UPLOAD_PATH = "images/ckeditor/"
MEDIA_ROOT = '%s/travelapp/static/' % BASE_DIR

OAUTH2_INFO = {
    'client_id':'pvYUFjT6EM2DcP0hOTntCaVW853VZeMyslwwPdWb',
    'client_secret':'gXratf4uI0s2xD0m8aiMY2KOZmNa8N32RczrejiO64UrsjytUPZHmFAj226Iu6HbVv1lw7diRJjArSRF8iPgPQaxnazMLfjcrS8zSXRkzZpPrUuYN1JZ64hSlCe3thVH'
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

INTERNAL_IPS = [
    '127.0.0.1'
    ]
ROOT_URLCONF = 'travelproject.urls'

#cloudinary config
cloudinary.config(
  cloud_name = "dec25",
  api_key = "752682513512722",
  api_secret = "P6Sb5YZCvBFpcMYAyumZnIpewNU"
)
# CLOUDINARY_STORAGE = {
#       'CLOUD_NAME': 'dec25',
#       'API_KEY': '752682513512722',
#       'API_SECRET': 'P6Sb5YZCvBFpcMYAyumZnIpewNU',
# }
# MEDIA_URL = '/TRAVELAGENCYOU/'
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


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

WSGI_APPLICATION = 'travelproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'travelappdb',
        'USER': 'root',
        'PASSWORD': '25122k',
        'HOST': '' # mặc định localhost
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    )
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#send mail config
#
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'travel.agency.ou@gmail.com'
# EMAIL_HOST_PASSWORD = '25122000Thu@'
# DEFAULT_FROM_EMAIL = 'travel.agency.ou@gmail.com'
# DEFAULT_TO_EMAIL = 'travel.agency.ou@gmail.com'


#send mail config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'travel.agency.ou@gmail.com'
EMAIL_HOST_PASSWORD = '25122000Thu@'
EMAIL_PORT = 587

#auth-social config
GOOGLE_CLIENT_ID = '907257214038-g3facenq9qtd3m8j670v46v7t7dppu4o.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
SOCIAL_SECRET = '@gbklknspajdoughwblwdoiushuolnjhsuyu5w#@#%$'
# Facebook
# appId = "3126040770995876"


# OAUTH2_PROVIDER = {
#     'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore'
# }