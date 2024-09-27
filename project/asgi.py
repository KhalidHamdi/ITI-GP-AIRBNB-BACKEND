"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.auth import  AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import  AllowedHostsOriginValidator

from django.core.asgi import get_asgi_application



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_asgi_application()

from chat import routing 
from chat.token_auth  import TokenAuthMiddleware

application = ProtocolTypeRouter({
    "http": get_asgi_application(), 
    "websocket": TokenAuthMiddleware(
        AllowedHostsOriginValidator(
            URLRouter(
                routing.websocket_urlpatterns 
            )
        )
    ),
})

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AllowedHostsOriginValidator(
#         URLRouter(
#             routing.websocket_urlpatterns 
#         )
#     ),
# })