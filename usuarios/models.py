from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel          # <-- importar
from django.core.files.storage import default_storage
from django.utils import timezone
from datetime import timedelta

from productos.models import Grupo, SubGrupo

class Vendedor(TimeStampedModel):                # <-- hereda de TimeStampedModel
    user      = models.OneToOneField(User, on_delete=models.CASCADE)
    grupos    = models.ManyToManyField(Grupo,    blank=True)
    subgrupos = models.ManyToManyField(SubGrupo, blank=True)
    presupuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0,help_text="Presupuesto mensual asignado")
    def __str__(self):
        return self.user.username

class UserProfile(models.Model):
    """Perfil extendido del usuario"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
    
    def __str__(self):
        return f"Perfil de {self.user.get_full_name() or self.user.username}"
    
    def get_profile_picture_url(self):
        """Obtener URL de la foto de perfil"""
        if self.profile_picture and default_storage.exists(self.profile_picture):
            return default_storage.url(self.profile_picture)
        return None
    
    def get_initials(self):
        """Obtener iniciales del usuario para mostrar cuando no hay foto"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name[0]}{self.user.last_name[0]}".upper()
        elif self.user.first_name:
            return self.user.first_name[0].upper()
        else:
            return self.user.username[0].upper()



class MensajeJefeVentas(TimeStampedModel):
    """Mensajes del jefe de ventas a vendedores"""
    
    class TipoMensaje(models.TextChoices):
        MOTIVACIONAL = 'M', 'Motivacional'
        ALERTA = 'A', 'Alerta'
        FELICITACION = 'F', 'Felicitación'
        RECORDATORIO = 'R', 'Recordatorio'
        REUNION = 'RE', 'Reunión'
    
    class Prioridad(models.TextChoices):
        BAJA = 'B', 'Baja'
        MEDIA = 'M', 'Media'
        ALTA = 'A', 'Alta'
        URGENTE = 'U', 'Urgente'
    
    jefe = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mensajes_enviados',
        help_text="Jefe de ventas que envía el mensaje"
    )
    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.CASCADE,
        related_name='mensajes_recibidos'
    )
    tipo = models.CharField(
        max_length=2,
        choices=TipoMensaje.choices,
        default=TipoMensaje.MOTIVACIONAL
    )
    prioridad = models.CharField(
        max_length=1,
        choices=Prioridad.choices,
        default=Prioridad.MEDIA
    )
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    leido = models.BooleanField(default=False)
    fecha_leido = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Mensaje de Jefe de Ventas'
        verbose_name_plural = 'Mensajes de Jefe de Ventas'
    
    def __str__(self):
        return f"{self.asunto} - {self.vendedor.user.username}"

class MetaVendedor(TimeStampedModel):
    """Metas específicas asignadas por el jefe de ventas"""
    
    class TipoMeta(models.TextChoices):
        MENSUAL = 'M', 'Mensual'
        TRIMESTRAL = 'T', 'Trimestral'
        ANUAL = 'A', 'Anual'
        PERSONALIZADA = 'P', 'Personalizada'
    
    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.CASCADE,
        related_name='metas_asignadas'
    )
    asignada_por = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='metas_asignadas',
        help_text="Jefe que asignó la meta"
    )
    tipo = models.CharField(
        max_length=1,
        choices=TipoMeta.choices,
        default=TipoMeta.MENSUAL
    )
    monto_meta = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Meta de Vendedor'
        verbose_name_plural = 'Metas de Vendedores'
    
    def __str__(self):
        return f"Meta {self.get_tipo_display()} - {self.vendedor.user.username}"
    
    @property
    def progreso_actual(self):
        """Calcula el progreso actual de la meta"""
        from pedidos.models import Pedido
        from django.db.models import Sum
        
        ventas = Pedido.objects.filter(
            vendedor=self.vendedor,
            fecha__gte=self.fecha_inicio,
            fecha__lte=self.fecha_fin,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).aggregate(total=Sum('total'))['total'] or 0
        
        return ventas
    
    @property
    def porcentaje_cumplimiento(self):
        """Porcentaje de cumplimiento de la meta"""
        if self.monto_meta > 0:
            return float((self.progreso_actual / self.monto_meta * 100))
        return 0

class SeguimientoVendedor(TimeStampedModel):
    """Seguimiento detallado del rendimiento de vendedores"""
    
    class TipoSeguimiento(models.TextChoices):
        REUNION = 'R', 'Reunión'
        EVALUACION = 'E', 'Evaluación'
        COACHING = 'C', 'Coaching'
        REVISION = 'RE', 'Revisión'
    
    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.CASCADE,
        related_name='seguimientos'
    )
    realizado_por = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='seguimientos_realizados'
    )
    tipo = models.CharField(
        max_length=2,
        choices=TipoSeguimiento.choices,
        default=TipoSeguimiento.REVISION
    )
    fecha_seguimiento = models.DateTimeField()
    observaciones = models.TextField()
    puntos_fuertes = models.TextField(blank=True, null=True)
    areas_mejora = models.TextField(blank=True, null=True)
    acciones_acordadas = models.TextField(blank=True, null=True)
    calificacion = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="Calificación del 1 al 5",
        null=True,
        blank=True
    )
    
    class Meta:
        ordering = ['-fecha_seguimiento']
        verbose_name = 'Seguimiento de Vendedor'
        verbose_name_plural = 'Seguimientos de Vendedores'
    
    def __str__(self):
        return f"Seguimiento {self.get_tipo_display()} - {self.vendedor.user.username}"

class PresupuestoMensual(TimeStampedModel):
    """Presupuestos mensuales específicos para cada vendedor"""
    
    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.CASCADE,
        related_name='presupuestos_mensuales'
    )
    
    asignado_por = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='presupuestos_asignados',
        help_text="Jefe que asignó este presupuesto"
    )
    
    año = models.IntegerField(help_text="Año del presupuesto")
    mes = models.IntegerField(
        choices=[
            (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
            (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
            (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
        ],
        help_text="Mes del presupuesto"
    )
    
    monto_presupuesto = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        help_text="Monto del presupuesto para este mes específico"
    )
    
    observaciones = models.TextField(
        blank=True, 
        null=True,
        help_text="Notas sobre este presupuesto (ej: temporada alta, promociones, etc.)"
    )
    
    activo = models.BooleanField(
        default=True,
        help_text="Si este presupuesto está activo para el mes correspondiente"
    )
    
    class Meta:
        ordering = ['-año', '-mes']
        verbose_name = 'Presupuesto Mensual'
        verbose_name_plural = 'Presupuestos Mensuales'
        unique_together = ['vendedor', 'año', 'mes']  # Un presupuesto por vendedor por mes
    
    def __str__(self):
        return f"{self.vendedor.user.username} - {self.get_mes_display()} {self.año}: ${self.monto_presupuesto:,.0f}"
    
    @property
    def ventas_reales(self):
        """Calcula las ventas reales para este mes específico"""
        from pedidos.models import Pedido
        from django.db.models import Sum
        from datetime import date
        
        inicio_mes = date(self.año, self.mes, 1)
        if self.mes == 12:
            fin_mes = date(self.año + 1, 1, 1) - timedelta(days=1)
        else:
            fin_mes = date(self.año, self.mes + 1, 1) - timedelta(days=1)
        
        ventas = Pedido.objects.filter(
            vendedor=self.vendedor,
            fecha__gte=inicio_mes,
            fecha__lte=fin_mes,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).aggregate(total=Sum('total'))['total'] or 0
        
        return ventas
    
    @property
    def porcentaje_cumplimiento(self):
        """Porcentaje de cumplimiento del presupuesto"""
        if self.monto_presupuesto > 0:
            return float((self.ventas_reales / self.monto_presupuesto * 100))
        return 0
    
    @property
    def diferencia(self):
        """Diferencia entre ventas reales y presupuesto"""
        return self.ventas_reales - self.monto_presupuesto
    
    @property
    def estado_cumplimiento(self):
        """Estado del cumplimiento del presupuesto"""
        porcentaje = self.porcentaje_cumplimiento
        if porcentaje >= 100:
            return 'completado'
        elif porcentaje >= 80:
            return 'en_progreso_alto'
        elif porcentaje >= 50:
            return 'en_progreso_medio'
        else:
            return 'bajo'

class EventoAgenda(TimeStampedModel):
    """Eventos de agenda para vendedores"""
    
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
        Vendedor,
        on_delete=models.CASCADE,
        related_name='eventos_agenda'
    )
    
    # Vendedores adicionales para reuniones grupales
    vendedores_adicionales = models.ManyToManyField(
        Vendedor,
        blank=True,
        related_name='eventos_adicionales',
        help_text="Vendedores adicionales invitados a la reunión"
    )
    
    # Gestor que creó el evento (para tracking)
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos_creados',
        help_text="Usuario que creó este evento"
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
        'clientes.Cliente',
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
        return self.fecha_inicio.date() == timezone.now().date()
    
    @property
    def es_urgente(self):
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
