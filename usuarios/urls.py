from django.urls import path
from .views import dashboard_vendedor, dashboard_gestor, dashboard_jefeventas, dashboard_redirect
from .profile_views import profile_view, update_profile, change_password, upload_profile_picture
from .notification_views import get_notifications, mark_notification_read, mark_all_notifications_read, get_notification_count
from .agenda_views import mi_agenda, crear_evento_agenda, ajax_eventos_agenda, marcar_evento_completado, ajax_buscar_clientes_agenda, crear_reunion, agendar_cita
from .calculadora_views import calculadora_precios, ajax_calcular_precio
from .inbox_views import inbox_mensajes, detalle_mensaje, marcar_mensaje_leido, marcar_mensaje_no_leido, marcar_todos_leidos, get_mensajes_count
from .views_gestor import todos_los_pedidos, actualizar_bd_clientes, inventario_general, subir_bd_productos
from .jefe_ventas_views import (
    dashboard_jefeventas_completo, dashboard_jefeventas_completo_test, detalle_vendedor, enviar_mensaje_vendedor,
    asignar_meta_vendedor, crear_seguimiento_vendedor, reportes_equipo, mi_equipo, presupuestos_metas,
    actualizar_presupuesto_vendedor, presupuestos_mensuales, crear_presupuesto_mensual, mensajes_equipo,
    enviar_mensaje_grupal
)
from .jefe_ventas_views_simple import dashboard_jefeventas_completo_simple
from productos.views_temp import actualizar_bd_productos_gestor_temp as actualizar_bd_productos_gestor


app_name = 'usuarios' 

urlpatterns = [
    # Dashboards
    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/vendedor/', dashboard_vendedor, name='dashboard_vendedor'),
    path('dashboard/gestor/', dashboard_gestor, name='dashboard_gestor'),
    path('dashboard/jefeventas/', dashboard_jefeventas, name='dashboard_jefeventas'),
    
    # Dashboard completo de jefe de ventas
    path('dashboard/jefeventas/completo/', dashboard_jefeventas_completo, name='dashboard_jefeventas_completo'),
    path('dashboard/jefeventas/test/', dashboard_jefeventas_completo_test, name='dashboard_jefeventas_test'),
    path('dashboard/jefeventas/simple/', dashboard_jefeventas_completo_simple, name='dashboard_jefeventas_simple'),
    path('vendedor/<int:vendedor_id>/detalle/', detalle_vendedor, name='detalle_vendedor'),
    path('reportes/equipo/', reportes_equipo, name='reportes_equipo'),
    
    # Gestión del equipo
    path('mi-equipo/', mi_equipo, name='mi_equipo'),
    path('presupuestos-metas/', presupuestos_metas, name='presupuestos_metas'),
    path('presupuestos-mensuales/', presupuestos_mensuales, name='presupuestos_mensuales'),
    path('mensajes-equipo/', mensajes_equipo, name='mensajes_equipo'),
    path('api/actualizar-presupuesto/', actualizar_presupuesto_vendedor, name='actualizar_presupuesto_vendedor'),
    path('api/crear-presupuesto-mensual/', crear_presupuesto_mensual, name='crear_presupuesto_mensual'),
    path('api/enviar-mensaje-grupal/', enviar_mensaje_grupal, name='enviar_mensaje_grupal'),
    
    # Funciones de gestión de jefe de ventas
    path('api/enviar-mensaje-vendedor/', enviar_mensaje_vendedor, name='enviar_mensaje_vendedor'),
    path('api/asignar-meta-vendedor/', asignar_meta_vendedor, name='asignar_meta_vendedor'),
    path('api/crear-seguimiento-vendedor/', crear_seguimiento_vendedor, name='crear_seguimiento_vendedor'),
    
    # Perfil de usuario
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/change-password/', change_password, name='change_password'),
    path('profile/upload-picture/', upload_profile_picture, name='upload_profile_picture'),
    
    # Notificaciones API
    path('api/notifications/', get_notifications, name='api_notifications'),
    path('api/notifications/<int:notification_id>/read/', mark_notification_read, name='mark_notification_read'),
    path('api/notifications/mark-all-read/', mark_all_notifications_read, name='mark_all_notifications_read'),
    path('api/notifications/count/', get_notification_count, name='notification_count'),
    
    # Herramientas del Vendedor
    path('calculadora-precios/', calculadora_precios, name='calculadora_precios'),
    path('calculadora-precios/calcular/', ajax_calcular_precio, name='ajax_calcular_precio'),
    path('mi-agenda/', mi_agenda, name='mi_agenda'),
    path('agenda/crear-evento/', crear_evento_agenda, name='crear_evento_agenda'),
    path('agenda/eventos/', ajax_eventos_agenda, name='ajax_eventos_agenda'),
    path('agenda/buscar-clientes/', ajax_buscar_clientes_agenda, name='ajax_buscar_clientes_agenda'),
    path('agenda/completar/<int:evento_id>/', marcar_evento_completado, name='marcar_evento_completado'),
    
    # Funcionalidades específicas de agenda
    path('agenda/crear-reunion/', crear_reunion, name='crear_reunion'),
    path('agenda/agendar-cita/', agendar_cita, name='agendar_cita'),
    
    # Sistema de Mensajes - Inbox
    path('inbox/', inbox_mensajes, name='inbox_mensajes'),
    path('inbox/mensaje/<int:mensaje_id>/', detalle_mensaje, name='detalle_mensaje'),
    path('inbox/mensaje/<int:mensaje_id>/marcar-leido/', marcar_mensaje_leido, name='marcar_mensaje_leido'),
    path('inbox/mensaje/<int:mensaje_id>/marcar-no-leido/', marcar_mensaje_no_leido, name='marcar_mensaje_no_leido'),
    path('inbox/marcar-todos-leidos/', marcar_todos_leidos, name='marcar_todos_leidos'),
    path('api/mensajes/count/', get_mensajes_count, name='get_mensajes_count'),
    
    # Funciones del Gestor
    path('gestor/pedidos/', todos_los_pedidos, name='todos_los_pedidos'),
    path('gestor/clientes/actualizar/', actualizar_bd_clientes, name='actualizar_bd_clientes'),
    path('gestor/inventario/', inventario_general, name='inventario_general'),
    path('gestor/productos/subir/', actualizar_bd_productos_gestor, name='subir_bd_productos'),
]
