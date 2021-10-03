"""
ASGI config for notification project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from notification.routing import websocket_urlpatterns
#from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack



#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.dev')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.pro')
django.setup()
from .middleware.channelsmiddleware import JwtAuthMiddlewareStack


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
           websocket_urlpatterns
        )
    
    ),
    
})
