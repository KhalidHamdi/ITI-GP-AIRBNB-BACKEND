# useraccount/context_processors.py

from django.conf import settings

def website_url(request):
    return {
        'website_url': settings.WEBSITE_URL
    }
