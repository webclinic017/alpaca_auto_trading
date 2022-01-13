from .base import *


DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases



STATIC_URL = '/static/'

# Follow https://docs.djangoproject.com/en/4.0/howto/static-files/
# to serve static files in production environment
#
# !! DO NOT USE THE FOLLOWING SETTINGS FOR STATIC FILES DIRECTORY
# IN PRODUCTION ENVIRONMENT !!
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': os.getenv('DBNAME'),  # dbname
        'USER': os.getenv('DBUSER'),
        'PASSWORD': os.getenv('DBPASSWORD'),
        'HOST': os.getenv('DBHOST'),
        'PORT': 5432,
    },
    

}