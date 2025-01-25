from .base import *

from decouple import config


SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool, default=True)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DJANGO_LOCAL_DB_NAME'),
        'USER': config('DJANGO_LOCAL_DB_USER'),
        'PASSWORD': config('DJANGO_LOCAL_DB_PASSWORD'),
        'HOST': config('DJANGO_LOCAL_DB_HOST', '127.0.0.1'),
        'PORT': config('DJANGO_LOCAL_DB_PORT', 5432),
    }, }
