from django.contrib import admin
from .models import Pedido, ItemPedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display   = ('pk','cliente','fecha','estado','total')
    list_filter    = ('estado','fecha')
    search_fields  = ('cliente__data__Empresa','pk')

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display  = ('pedido','producto','cantidad','subtotal')
    list_filter   = ('producto',)
