from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils import translation
from django.conf import settings
from django import template
from django.utils.translation import activate

def home_view(request):
    greeting = _("Hello, world!")
    return render(request, 'home.html', {'greeting': greeting})


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = request.GET.get('language')
        if language and language in settings.LANGUAGES:
            translation.activate(language)
            request.LANGUAGE_CODE = language

        response = self.get_response(request)

        return response
    
    MIDDLEWARE = [
    # ... other middleware classes
    'path.to.middleware.LanguageMiddleware',
]
    

register = template.Library()

@register.simple_tag
def set_language(language):
    activate(language)
    return ''