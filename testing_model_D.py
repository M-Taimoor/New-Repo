# settings.py

INSTALLED_APPS = [
    # ... other apps ...
    'products',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Localization and internationalization
    'django.middleware.locale.LocaleMiddleware',
]

MIDDLEWARE = [
    # ... other middleware ...
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Languages supported by the site
LANGUAGES = [
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('de', 'German'),
]

# Default language
LANGUAGE_CODE = 'en'

# Locale path
LOCALE_PATHS = [BASE_DIR / 'locale']