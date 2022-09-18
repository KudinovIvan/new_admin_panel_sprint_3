import os
from pathlib import Path
from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

include(
    'components/apps.py',
    'components/middleware.py',
    'components/database.py',
    'components/templates.py',
    'components/validators.py',
    'components/static_and_media.py',
)

SECRET_KEY = os.environ.get('SECRET_KEY')

CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']

DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

LANGUAGE_CODE = 'ru-RU'

LOCALE_PATHS = ['movies/locale']

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
