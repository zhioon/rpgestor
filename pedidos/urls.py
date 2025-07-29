from django.urls import path
from .views import (
    crear_pedido,
    ajax_buscar_cliente,
    ajax_price_types,
    ajax_productos,
    confirmar_pedido,
    detalle_pedido,
    finalizar_pedido,
    enviar_pedido_gestor,
    enviar_pedido_cliente,
    descargar_csv,
    mis_pedidos,
    historial_cliente,
)

app_name = 'pedidos'   # <-- esencial para que namespace funcione

urlpatterns = [
    path('ajax/buscar-cliente/', 
         ajax_buscar_cliente, name='ajax_buscar_cliente'),
    path('ajax/price-types/<int:cliente_id>/', 
         ajax_price_types,    name='ajax_price_types'),
    path('ajax/productos/<int:cliente_id>/<int:price_type>/',
         ajax_productos,      name='ajax_productos'),

    path('nuevo/',         crear_pedido,    name='crear_pedido'),
    path('mis-pedidos/',   mis_pedidos,     name='mis_pedidos'),
    path('confirmar/', confirmar_pedido, name='confirmar_pedido'),
    path('<int:pk>/',      detalle_pedido,  name='detalle_pedido'),
    path('<int:pk>/finalizar/', finalizar_pedido, name='finalizar_pedido'),
    path('<int:pk>/enviar-gestor/',  enviar_pedido_gestor,  name='enviar_pedido_gestor'),
    path('<int:pk>/enviar-cliente/', enviar_pedido_cliente, name='enviar_pedido_cliente'),
    path('<int:pk>/csv/',            descargar_csv,         name='descargar_csv'),
    path('cliente/<int:cliente_id>/historial/', historial_cliente, name='historial_cliente'),
]
