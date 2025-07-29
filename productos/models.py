from django.db import models
from core.models import TimeStampedModel
from django.contrib.auth.models import User

class Grupo(TimeStampedModel):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class SubGrupo(TimeStampedModel):
    nombre = models.CharField(max_length=100)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('nombre', 'grupo')

    def __str__(self):
        return f"{self.grupo} – {self.nombre}"

class Producto(TimeStampedModel):
    grupo      = models.ForeignKey(Grupo,   on_delete=models.PROTECT)
    subgrupo   = models.ForeignKey(SubGrupo,on_delete=models.PROTECT)
    codigo     = models.CharField(max_length=50, unique=True)
    nombre     = models.CharField(max_length=255)
    imagen     = models.ImageField(upload_to='productos/', null=True, blank=True)
    iva        = models.DecimalField(max_digits=5,  decimal_places=2)
    descuento  = models.DecimalField(max_digits=5,  decimal_places=2)
    precio1    = models.DecimalField(max_digits=12, decimal_places=2)
    precio2    = models.DecimalField(max_digits=12, decimal_places=2)
    precio3    = models.DecimalField(max_digits=12, decimal_places=2)
    precio4    = models.DecimalField(max_digits=12, decimal_places=2)
    precio5    = models.DecimalField(max_digits=12, decimal_places=2)
    precio6    = models.DecimalField(max_digits=12, decimal_places=2)
    stock      = models.IntegerField()
    externo_id = models.CharField(max_length=50)  # para el campo “id” de Excel

    def __str__(self):
        return f"{self.codigo} – {self.nombre}"

class StockMovimiento(models.Model):
    TIPOS = [
        ('ENT', 'Entrada'),
        ('SAL', 'Salida'),
    ]
    producto    = models.ForeignKey('Producto', on_delete=models.PROTECT, related_name='movimientos')
    tipo        = models.CharField(max_length=3, choices=TIPOS)
    cantidad    = models.PositiveIntegerField()
    fecha       = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notas       = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.get_tipo_display()} {self.cantidad} de {self.producto.codigo}"