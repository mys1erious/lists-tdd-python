from .base import *


DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../database/db.sqlite3')
    }
}

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../collectedstatic'))

ALLOWED_HOSTS = []
