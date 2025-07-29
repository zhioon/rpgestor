from decimal import Decimal
from django.db import models
from core.models import TimeStampedModel
from clientes.models import Cliente
from productos.models import Producto
from usuarios.models import Vendedor  # ← Nuevo import

class Pedido(TimeStampedModel):
    class Estado(models.TextChoices):
        BORRADOR  = 'B', 'Borrador'
        ENVIADO   = 'E', 'Enviado'
        FINALIZADO = 'F', 'Finalizado'
        CANCELADO = 'C', 'Cancelado'

    cliente    = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    vendedor   = models.ForeignKey(               # ← Nuevo campo
        Vendedor,
        on_delete=models.PROTECT,
        related_name='pedidos',
        null=True,
        blank=True
    )
    fecha      = models.DateField(auto_now_add=True)
    estado     = models.CharField(
        max_length=1, choices=Estado.choices, default=Estado.BORRADOR
    )
    nota       = models.TextField(blank=True, null=True, help_text="Nota adicional del pedido")
    iva_total  = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total      = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido {self.pk} – {self.cliente}"

class ItemPedido(TimeStampedModel):
    pedido          = models.ForeignKey(
        Pedido, related_name='items', on_delete=models.CASCADE
    )
    producto        = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad        = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    descuento       = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    subtotal        = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        discount_factor = (Decimal('1') - (self.descuento / Decimal('100')))
        net_price = self.precio_unitario * discount_factor
        self.subtotal = net_price * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"
