# notificaciones/urls.py
from django.urls import path
from .views import inbox, enviar_mensaje, detalle_mensaje, test_websocket

app_name = 'notificaciones'

urlpatterns = [
    path('mensajes/',            inbox,           name='inbox'),
    path('mensajes/nuevo/',      enviar_mensaje,  name='enviar'),
    path('mensajes/<int:pk>/',   detalle_mensaje, name='detalle'),
    path('test-websocket/',      test_websocket,  name='test_websocket'),
]
