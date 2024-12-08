# settings.py
from django.utils.translation import gettext_lazy as _

# Internationalization settings
LANGUAGE_CODE = "en-us"  # Default language
USE_I18N = True  # Enable internationalization
USE_L10N = True  # Enable localization
USE_TZ = True  # Enable time zone support

LANGUAGES = [
    ("en", _("English")),
    ("es", _("Spanish")),
    ("fr", _("French")),
    # Add more languages as needed
]

LOCALE_PATHS = [
    BASE_DIR / "locale",  # Path to store translation files
]

# Middleware for setting the language
MIDDLEWARE = [
    # ...
    "django.middleware.locale.LocaleMiddleware",  # Enable locale middleware
    # ...
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Add this to allow serving static files during development
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"