
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.getenv('DJANGO_DEBUG', 0) != 'False'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
ALLOWED_HOSTS_ENV = os.environ.get('ALLOWED_HOSTS')
if ALLOWED_HOSTS_ENV:
    ALLOWED_HOSTS.extend(ALLOWED_HOSTS_ENV.split(','))



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tradingview.apps.TradingviewConfig',
    'django_apscheduler',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tradingview.helpers.SyncLog',
]

ROOT_URLCONF = 'tradingview_clone.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tradingview_clone.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("MYSQL_DB"),
        'USER': os.getenv("MYSQL_USER"),
        'PASSWORD': os.getenv("MYSQL_PASSWORD"),
        'PORT': os.getenv("MYSQL_PORT"),
        'HOST': os.getenv("MYSQL_HOST"),
        'DB_IGNORE_SSL': os.getenv("DB_IGNORE_SSL") == "true",
        'OPTIONS': {
            # 'init_command': 'SET default_storage_engine=INNODB',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1",
            'charset': 'utf8mb4',
            "autocommit": True,
        }
    }
}


# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    #BASE_DIR/ 'staticfiles',
    BASE_DIR/ 'tradingview' / 'static',
]


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"  # Default

SCHEDULER_DEFAULT = True
