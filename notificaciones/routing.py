from django.urls import re_path
from .consumers import AppConsumer

websocket_urlpatterns = [
    re_path(r'ws/notificaciones/$', AppConsumer.as_asgi()),
]
