"""
Django settings for the Django Async project.
"""
import os
import dj_database_url

from django_chat.apps.bot.apps import BotConfig
from django_chat.apps.chat.apps import ChatConfig
from django_chat.apps.web.apps import WebConfig
from django_chat.utils import env2bool
from pythonjsonlogger.jsonlogger import JsonFormatter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if DJANGO_SECRET_KEY:
    SECRET_KEY = DJANGO_SECRET_KEY
else:
    raise NotImplementedError("You must configure DJANGO_SECRET_KEY!")

CSRF_COOKIE_SECURE = env2bool("CSRF_COOKIE_SECURE", False)
SESSION_COOKIE_SECURE = env2bool("SESSION_COOKIE_SECURE", False)

DEBUG = env2bool("DJANGO_SETTINGS_DEBUG", True)

DJANGO_ALLOWED_HOSTS: str = os.getenv("DJANGO_ALLOWED_HOSTS", "*")

if DJANGO_ALLOWED_HOSTS:
    ALLOWED_HOSTS = DJANGO_ALLOWED_HOSTS.split(",")
else:
    ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "channels",  # ASGI absctraction layer must come first --> takes control over manage.py
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    WebConfig.name,
    ChatConfig.name,
    BotConfig.name,
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_chat.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,  # look for template files inside the apps
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

# WSGI application
# WSGI_APPLICATION = "django_chat.wsgi.application"

# ASGI application (protocol router)
ASGI_APPLICATION = "django_chat.routing.application"

# Database
DATABASES = {
	"default": dj_database_url.config() # Parse DB credentials from the DATABASE_URL env
}

DATABASES["default"]["CONN_MAX_AGE"] = int(os.getenv("DB_CONN_MAX_AGE", 0))  # type: ignore

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "()": JsonFormatter,
            "format": "%(levelname)-8s [%(asctime)s] [%(request_id)s] %(name)s: %(message)s",
        }
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "standard"}},
    "loggers": {"": {"level": os.getenv("ROOT_LOG_LEVEL", "INFO"), "handlers": ["console"]},},
}

# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"

# Channels LAYERS enabling
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [os.getenv("REDIS_URL", "redis://redis:6379")]},
    }
}
WORKER_CHANNEL_NAME = os.getenv("WORKER_CHANNEL")
BOT_USER_NAME = "🤖 DJANGO BOT 🤖"
