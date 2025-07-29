from django.urls import path
from .views import (
    import_clients_full,
    lista_clientes,
    clientes_favoritos,
    toggle_favorito,
    detalle_cliente,
)

app_name = 'clientes'

urlpatterns = [
    path('import-clients-full/', import_clients_full, name='import_clients_full'),
    path('lista/', lista_clientes, name='lista_clientes'),
    path('favoritos/', clientes_favoritos, name='clientes_favoritos'),
    path('toggle-favorito/<int:cliente_id>/', toggle_favorito, name='toggle_favorito'),
    path('detalle/<int:cliente_id>/', detalle_cliente, name='detalle_cliente'),
]
