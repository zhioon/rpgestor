from django.contrib import admin
from .models import Vendedor, UserProfile, EventoAgenda, MensajeJefeVentas, MetaVendedor, SeguimientoVendedor

@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('user','presupuesto','created_at','updated_at')
    filter_horizontal = ('grupos','subgrupos')
    search_fields = ['user__username', 'user__first_name', 'user__last_name']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Información del Perfil', {
            'fields': ('profile_picture', 'phone')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(EventoAgenda)
class EventoAgendaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'vendedor', 'tipo', 'prioridad', 'estado', 'fecha_inicio']
    list_filter = ['tipo', 'prioridad', 'estado', 'fecha_inicio', 'created_at']
    search_fields = ['titulo', 'descripcion', 'vendedor__user__username']
    date_hierarchy = 'fecha_inicio'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('vendedor', 'titulo', 'descripcion', 'tipo', 'prioridad', 'estado')
        }),
        ('Fechas y Horarios', {
            'fields': ('fecha_inicio', 'fecha_fin', 'ubicacion')
        }),
        ('Cliente y Recordatorios', {
            'fields': ('cliente', 'recordatorio_enviado', 'minutos_recordatorio')
        }),
        ('Participantes Adicionales', {
            'fields': ('vendedores_adicionales', 'creado_por')
        }),
        ('Notas', {
            'fields': ('notas',)
        })
    )
    
    filter_horizontal = ['vendedores_adicionales']

@admin.register(MensajeJefeVentas)
class MensajeJefeVentasAdmin(admin.ModelAdmin):
    list_display = ['asunto', 'jefe', 'vendedor', 'tipo', 'prioridad', 'leido', 'created_at']
    list_filter = ['tipo', 'prioridad', 'leido', 'created_at']
    search_fields = ['asunto', 'mensaje', 'jefe__username', 'vendedor__user__username']
    readonly_fields = ['created_at', 'updated_at', 'fecha_leido']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información del Mensaje', {
            'fields': ('jefe', 'vendedor', 'tipo', 'prioridad', 'asunto', 'mensaje')
        }),
        ('Estado', {
            'fields': ('leido', 'fecha_leido')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(MetaVendedor)
class MetaVendedorAdmin(admin.ModelAdmin):
    list_display = ['vendedor', 'tipo', 'monto_meta', 'fecha_inicio', 'fecha_fin', 'get_porcentaje_cumplimiento', 'activa']
    list_filter = ['tipo', 'activa', 'fecha_inicio', 'fecha_fin', 'created_at']
    search_fields = ['vendedor__user__username', 'vendedor__user__first_name', 'vendedor__user__last_name', 'descripcion']
    readonly_fields = ['created_at', 'updated_at', 'get_progreso_actual', 'get_porcentaje_cumplimiento']
    date_hierarchy = 'fecha_inicio'
    
    fieldsets = (
        ('Información de la Meta', {
            'fields': ('vendedor', 'asignada_por', 'tipo', 'monto_meta', 'descripcion')
        }),
        ('Período', {
            'fields': ('fecha_inicio', 'fecha_fin', 'activa')
        }),
        ('Progreso', {
            'fields': ('get_progreso_actual', 'get_porcentaje_cumplimiento'),
            'classes': ('collapse',)
        }),
        ('Fechas del Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_progreso_actual(self, obj):
        return f"${obj.progreso_actual:,.2f}"
    get_progreso_actual.short_description = 'Progreso Actual'
    
    def get_porcentaje_cumplimiento(self, obj):
        return f"{obj.porcentaje_cumplimiento:.1f}%"
    get_porcentaje_cumplimiento.short_description = 'Cumplimiento'

@admin.register(SeguimientoVendedor)
class SeguimientoVendedorAdmin(admin.ModelAdmin):
    list_display = ['vendedor', 'tipo', 'fecha_seguimiento', 'realizado_por', 'calificacion', 'created_at']
    list_filter = ['tipo', 'calificacion', 'fecha_seguimiento', 'created_at']
    search_fields = ['vendedor__user__username', 'vendedor__user__first_name', 'vendedor__user__last_name', 
                    'realizado_por__username', 'observaciones']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'fecha_seguimiento'
    
    fieldsets = (
        ('Información del Seguimiento', {
            'fields': ('vendedor', 'realizado_por', 'tipo', 'fecha_seguimiento', 'calificacion')
        }),
        ('Observaciones', {
            'fields': ('observaciones', 'puntos_fuertes', 'areas_mejora', 'acciones_acordadas')
        }),
        ('Fechas del Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
