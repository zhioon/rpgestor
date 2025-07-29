from django.db import models
from core.models import TimeStampedModel

class Cliente(TimeStampedModel):
    # Guarda todos los datos de la fila en un JSON
    data = models.JSONField()

    def __str__(self):
        # Muestra algo legible en el admin
        nombre = self.data.get('Empresa') or self.data.get('Razon_Comercial')
        return nombre or f"Cliente {self.pk}"

class ClienteFavorito(TimeStampedModel):
    """Modelo para manejar los clientes favoritos de cada vendedor"""
    vendedor = models.ForeignKey(
        'usuarios.Vendedor',
        on_delete=models.CASCADE,
        related_name='clientes_favoritos'
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='favorito_de'
    )
    
    class Meta:
        unique_together = ('vendedor', 'cliente')
        verbose_name = 'Cliente Favorito'
        verbose_name_plural = 'Clientes Favoritos'
    
    def __str__(self):
        return f"{self.vendedor.user.username} - {self.cliente}"

