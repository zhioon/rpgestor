from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel
from clientes.models import Cliente

class EventoAgenda(TimeStampedModel):
    class TipoEvento(models.TextChoices):
        VISITA = 'V', 'Visita a Cliente'
        LLAMADA = 'L', 'Llamada Telefónica'
        REUNION = 'R', 'Reunión'
        SEGUIMIENTO = 'S', 'Seguimiento'
        RECORDATORIO = 'RE', 'Recordatorio'
        OTRO = 'O', 'Otro'

    class Prioridad(models.TextChoices):
        BAJA = 'B', 'Baja'
        MEDIA = 'M', 'Media'
        ALTA = 'A', 'Alta'
        URGENTE = 'U', 'Urgente'

    class Estado(models.TextChoices):
        PENDIENTE = 'P', 'Pendiente'
        EN_PROGRESO = 'E', 'En Progreso'
        COMPLETADO = 'C', 'Completado'
        CANCELADO = 'CA', 'Cancelado'

    vendedor = models.ForeignKey(
        'usuarios.Vendedor',
        on_delete=models.CASCADE,
        related_name='eventos_agenda'
    )
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    
    tipo = models.CharField(
        max_length=2,
        choices=TipoEvento.choices,
        default=TipoEvento.VISITA
    )
    
    prioridad = models.CharField(
        max_length=1,
        choices=Prioridad.choices,
        default=Prioridad.MEDIA
    )
    
    estado = models.CharField(
        max_length=2,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )
    
    # Fechas y horarios
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(blank=True, null=True)
    
    # Cliente relacionado (opcional)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='eventos_agenda'
    )
    
    # Ubicación (opcional)
    ubicacion = models.CharField(max_length=300, blank=True, null=True)
    
    # Recordatorios
    recordatorio_enviado = models.BooleanField(default=False)
    minutos_recordatorio = models.IntegerField(
        default=30,
        help_text="Minutos antes del evento para enviar recordatorio"
    )
    
    # Notas adicionales
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['fecha_inicio']
        verbose_name = 'Evento de Agenda'
        verbose_name_plural = 'Eventos de Agenda'
    
    def __str__(self):
        return f"{self.titulo} - {self.fecha_inicio.strftime('%d/%m/%Y %H:%M')}"
    
    @property
    def es_hoy(self):
        from django.utils import timezone
        return self.fecha_inicio.date() == timezone.now().date()
    
    @property
    def es_urgente(self):
        from django.utils import timezone
        return (
            self.prioridad == self.Prioridad.URGENTE or
            (self.fecha_inicio <= timezone.now() + timezone.timedelta(hours=2) and 
             self.estado == self.Estado.PENDIENTE)
        )
    
    @property
    def color_prioridad(self):
        colores = {
            self.Prioridad.BAJA: 'bg-gray-100 text-gray-800',
            self.Prioridad.MEDIA: 'bg-blue-100 text-blue-800',
            self.Prioridad.ALTA: 'bg-yellow-100 text-yellow-800',
            self.Prioridad.URGENTE: 'bg-red-100 text-red-800',
        }
        return colores.get(self.prioridad, 'bg-gray-100 text-gray-800')
    
    @property
    def icono_tipo(self):
        iconos = {
            self.TipoEvento.VISITA: 'fas fa-map-marker-alt',
            self.TipoEvento.LLAMADA: 'fas fa-phone',
            self.TipoEvento.REUNION: 'fas fa-users',
            self.TipoEvento.SEGUIMIENTO: 'fas fa-eye',
            self.TipoEvento.RECORDATORIO: 'fas fa-bell',
            self.TipoEvento.OTRO: 'fas fa-calendar',
        }
        return iconos.get(self.tipo, 'fas fa-calendar')