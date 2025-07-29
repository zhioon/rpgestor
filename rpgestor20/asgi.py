import os
import django
from django.core.asgi import get_asgi_application

# Configurar Django ANTES de cualquier importación
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpgestor20.settings')

# Inicializar Django explícitamente
django.setup()

# Ahora podemos importar todo lo demás de forma segura
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import notificaciones.routing

# Crear la aplicación HTTP primero
django_asgi_app = get_asgi_application()

# Configurar el router de protocolos
application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            notificaciones.routing.websocket_urlpatterns
        )
    ),
})
