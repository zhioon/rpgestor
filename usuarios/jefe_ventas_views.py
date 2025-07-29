from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Sum, Count, Q, Avg, F, Max
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from calendar import monthrange
from decimal import Decimal
import json
import logging

from .models import Vendedor, MensajeJefeVentas, MetaVendedor, SeguimientoVendedor, PresupuestoMensual
from pedidos.models import Pedido, ItemPedido
from productos.models import Producto
from clientes.models import Cliente
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

def es_jefe_ventas(user):
    return user.is_authenticated and user.groups.filter(name='JefeVentas').exists()

def dashboard_jefeventas_completo_test(request):
    """Vista de prueba simple"""
    from django.http import HttpResponse
    return HttpResponse("<h1>PRUEBA EXITOSA</h1><p>Esta vista funciona correctamente</p>")

@user_passes_test(es_jefe_ventas, login_url='login')
def dashboard_jefeventas_completo(request):
    """Dashboard completo y mejorado para jefe de ventas"""
    
    # Fechas para cálculos
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    mes_anterior = (inicio_mes - timedelta(days=1)).replace(day=1)
    fin_mes_anterior = inicio_mes - timedelta(days=1)
    inicio_trimestre = hoy.replace(month=((hoy.month-1)//3)*3+1, day=1)
    
    # === ESTADÍSTICAS PRINCIPALES ===
    ventas_totales_mes = Pedido.objects.filter(
        fecha__gte=inicio_mes,
        estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).aggregate(total=Sum('total'))['total'] or Decimal('0')
    
    ventas_mes_anterior = Pedido.objects.filter(
        fecha__gte=mes_anterior,
        fecha__lte=fin_mes_anterior,
        estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).aggregate(total=Sum('total'))['total'] or Decimal('1')
    
    crecimiento_ventas = float(((ventas_totales_mes - ventas_mes_anterior) / ventas_mes_anterior * 100)) if ventas_mes_anterior > 0 else 0
    
    # Meta total del equipo usando presupuestos mensuales específicos
    meta_total_equipo = Decimal('0')
    for vendedor in Vendedor.objects.filter(user__groups__name='Vendedor'):
        presupuesto_mes_actual = PresupuestoMensual.objects.filter(
            vendedor=vendedor,
            año=hoy.year,
            mes=hoy.month,
            activo=True
        ).first()
        presupuesto_efectivo = presupuesto_mes_actual.monto_presupuesto if presupuesto_mes_actual else vendedor.presupuesto
        meta_total_equipo += presupuesto_efectivo
    
    porcentaje_meta_equipo = float((ventas_totales_mes / meta_total_equipo * 100)) if meta_total_equipo > 0 else 0
    
    # Estadísticas del equipo (solo vendedores del grupo "Vendedor")
    total_vendedores = Vendedor.objects.filter(user__groups__name='Vendedor').count()
    vendedores_activos = Vendedor.objects.filter(
        user__groups__name='Vendedor',
        pedidos__fecha__gte=inicio_mes,
        pedidos__estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).distinct().count()
    
    pedidos_totales_mes = Pedido.objects.filter(
        fecha__gte=inicio_mes,
        estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).count()
    
    # === ANÁLISIS DETALLADO DE VENDEDORES ===
    vendedores_detalle = []
    for vendedor in Vendedor.objects.select_related('user').prefetch_related('user__groups').filter(user__groups__name='Vendedor'):
        # Verificar que el vendedor tenga un usuario asociado
        if not vendedor.user:
            continue
        # Ventas del mes
        ventas_mes = Pedido.objects.filter(
            vendedor=vendedor,
            fecha__gte=inicio_mes,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
        
        # Ventas del mes anterior
        ventas_anterior = Pedido.objects.filter(
            vendedor=vendedor,
            fecha__gte=mes_anterior,
            fecha__lte=fin_mes_anterior,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
        
        # Pedidos del mes
        pedidos_mes = Pedido.objects.filter(
            vendedor=vendedor,
            fecha__gte=inicio_mes,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).count()
        
        # Clientes únicos atendidos
        clientes_unicos = Cliente.objects.filter(
            pedido__vendedor=vendedor,
            pedido__fecha__gte=inicio_mes,
            pedido__estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).distinct().count()
        
        # Promedio por pedido
        promedio_pedido = float(ventas_mes / pedidos_mes) if pedidos_mes > 0 else 0
        
        # Buscar presupuesto específico para el mes actual
        presupuesto_mes_actual = PresupuestoMensual.objects.filter(
            vendedor=vendedor,
            año=hoy.year,
            mes=hoy.month,
            activo=True
        ).first()
        
        # Usar presupuesto específico si existe, sino usar el presupuesto base
        presupuesto_efectivo = presupuesto_mes_actual.monto_presupuesto if presupuesto_mes_actual else vendedor.presupuesto
        
        # Porcentaje de cumplimiento con el presupuesto efectivo
        porcentaje_cumplimiento = float((ventas_mes / presupuesto_efectivo * 100)) if presupuesto_efectivo > 0 else 0
        
        # Crecimiento vs mes anterior
        crecimiento_individual = float(((ventas_mes - ventas_anterior) / ventas_anterior * 100)) if ventas_anterior > 0 else 0
        
        # Clasificación de rendimiento
        if porcentaje_cumplimiento >= 100:
            clasificacion = 'excelente'
            color_clasificacion = 'text-green-600'
        elif porcentaje_cumplimiento >= 80:
            clasificacion = 'bueno'
            color_clasificacion = 'text-blue-600'
        elif porcentaje_cumplimiento >= 60:
            clasificacion = 'regular'
            color_clasificacion = 'text-yellow-600'
        else:
            clasificacion = 'bajo'
            color_clasificacion = 'text-red-600'
        
        # Días sin ventas
        ultimo_pedido = Pedido.objects.filter(
            vendedor=vendedor,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).order_by('-fecha').first()
        
        dias_sin_ventas = (hoy - ultimo_pedido.fecha).days if ultimo_pedido else 999
        
        vendedores_detalle.append({
            'vendedor': vendedor,
            'ventas_mes': ventas_mes,
            'ventas_anterior': ventas_anterior,
            'pedidos_mes': pedidos_mes,
            'clientes_unicos': clientes_unicos,
            'promedio_pedido': promedio_pedido,
            'porcentaje_cumplimiento': porcentaje_cumplimiento,
            'crecimiento_individual': crecimiento_individual,
            'clasificacion': clasificacion,
            'color_clasificacion': color_clasificacion,
            'dias_sin_ventas': dias_sin_ventas,
            'necesita_atencion': porcentaje_cumplimiento < 50 or dias_sin_ventas > 7,
        })
    
    # Ordenar por ventas del mes
    vendedores_detalle.sort(key=lambda x: x['ventas_mes'], reverse=True)
    
    # === ALERTAS Y NOTIFICACIONES ===
    alertas = []
    
    # Vendedores con bajo rendimiento
    vendedores_bajo_rendimiento = [v for v in vendedores_detalle if v['porcentaje_cumplimiento'] < 50]
    if vendedores_bajo_rendimiento:
        alertas.append({
            'tipo': 'warning',
            'titulo': f'{len(vendedores_bajo_rendimiento)} vendedor(es) por debajo del 50% de meta',
            'descripcion': 'Requieren atención inmediata',
            'icono': 'fas fa-exclamation-triangle'
        })
    
    # Vendedores sin actividad reciente
    vendedores_inactivos = [v for v in vendedores_detalle if v['dias_sin_ventas'] > 7]
    if vendedores_inactivos:
        alertas.append({
            'tipo': 'danger',
            'titulo': f'{len(vendedores_inactivos)} vendedor(es) sin ventas en más de 7 días',
            'descripcion': 'Contactar urgentemente',
            'icono': 'fas fa-user-times'
        })
    
    # Vendedores destacados
    vendedores_destacados = [v for v in vendedores_detalle if v['porcentaje_cumplimiento'] >= 120]
    if vendedores_destacados:
        alertas.append({
            'tipo': 'success',
            'titulo': f'{len(vendedores_destacados)} vendedor(es) superando expectativas',
            'descripcion': 'Felicitar por excelente rendimiento',
            'icono': 'fas fa-trophy'
        })
    
    # === PRODUCTOS Y CLIENTES TOP ===
    productos_top_equipo = ItemPedido.objects.filter(
        pedido__fecha__gte=inicio_mes,
        pedido__estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).values(
        'producto__codigo',
        'producto__nombre'
    ).annotate(
        total_vendido=Sum('cantidad'),
        total_ingresos=Sum('subtotal'),
        num_vendedores=Count('pedido__vendedor', distinct=True)
    ).order_by('-total_vendido')[:5]
    
    clientes_importantes = Pedido.objects.filter(
        fecha__gte=inicio_mes,
        estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).values(
        'cliente__id',
        'cliente__data'
    ).annotate(
        total_compras=Sum('total'),
        num_pedidos=Count('id'),
        num_vendedores=Count('vendedor', distinct=True)
    ).order_by('-total_compras')[:5]
    
    # === DATOS PARA GRÁFICOS ===
    # Gráfico de ventas diarias
    dias_mes = monthrange(hoy.year, hoy.month)[1]
    ventas_diarias_equipo = []
    labels_dias = []
    
    for dia in range(1, min(dias_mes + 1, hoy.day + 1)):
        fecha_dia = hoy.replace(day=dia)
        ventas_dia = Pedido.objects.filter(
            fecha=fecha_dia,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).aggregate(total=Sum('total'))['total'] or 0
        
        ventas_diarias_equipo.append(float(ventas_dia))
        labels_dias.append(f"{dia}")
    
    # Gráfico comparativo de vendedores (top 5)
    top_5_vendedores = vendedores_detalle[:5]
    nombres_vendedores = [f"{v['vendedor'].user.first_name} {v['vendedor'].user.last_name}" for v in top_5_vendedores]
    ventas_vendedores = [float(v['ventas_mes']) for v in top_5_vendedores]
    # Usar presupuestos efectivos para el gráfico también
    metas_vendedores = []
    for v in top_5_vendedores:
        presupuesto_mes_actual = PresupuestoMensual.objects.filter(
            vendedor=v['vendedor'],
            año=hoy.year,
            mes=hoy.month,
            activo=True
        ).first()
        presupuesto_efectivo = presupuesto_mes_actual.monto_presupuesto if presupuesto_mes_actual else v['vendedor'].presupuesto
        metas_vendedores.append(float(presupuesto_efectivo))
    
    # === MENSAJES RECIENTES ===
    mensajes_recientes = MensajeJefeVentas.objects.filter(
        jefe=request.user
    ).select_related('vendedor__user').order_by('-created_at')[:5]
    
    # === PEDIDOS RECIENTES DEL EQUIPO ===
    pedidos_recientes = Pedido.objects.select_related(
        'cliente', 'vendedor__user'
    ).filter(vendedor__user__isnull=False).order_by('-created_at')[:8]
    
    context = {
        'user': request.user,
        'user_role': 'Jefe de Ventas',
        'dashboard_title': 'Dashboard Completo de Jefe de Ventas',
        
        # Estadísticas principales
        'ventas_totales_mes': ventas_totales_mes,
        'crecimiento_ventas': round(crecimiento_ventas, 1),
        'meta_total_equipo': meta_total_equipo,
        'porcentaje_meta_equipo': round(porcentaje_meta_equipo, 1),
        'pedidos_totales_mes': pedidos_totales_mes,
        'total_vendedores': total_vendedores,
        'vendedores_activos': vendedores_activos,
        
        # Análisis detallado
        'vendedores_detalle': vendedores_detalle,
        'alertas': alertas,
        'productos_top_equipo': productos_top_equipo,
        'clientes_importantes': clientes_importantes,
        'mensajes_recientes': mensajes_recientes,
        'pedidos_recientes': pedidos_recientes,
        
        # Datos para gráficos
        'ventas_diarias_equipo': ventas_diarias_equipo,
        'labels_dias': labels_dias,
        'nombres_vendedores': nombres_vendedores,
        'ventas_vendedores': ventas_vendedores,
        'metas_vendedores': metas_vendedores,
        'mes_actual': hoy.strftime('%B %Y'),
    }
    
    try:
        logger.info(f"Renderizando template con contexto: {list(context.keys())}")
        response = render(request, 'usuarios/dashboard_jefeventas.html', context)
        logger.info(f"Template renderizado exitosamente, tamaño: {len(response.content)} bytes")
        return response
    except Exception as e:
        logger.error(f"Error al renderizar template: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        # Devolver una respuesta simple en caso de error
        from django.http import HttpResponse
        return HttpResponse(f"<h1>Error en Dashboard</h1><p>Error: {str(e)}</p><pre>{traceback.format_exc()}</pre>")

@user_passes_test(es_jefe_ventas, login_url='login')
def detalle_vendedor(request, vendedor_id):
    """Vista detallada de un vendedor específico"""
    vendedor = get_object_or_404(Vendedor, id=vendedor_id)
    
    # Fechas para análisis
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    inicio_trimestre = hoy.replace(month=((hoy.month-1)//3)*3+1, day=1)
    inicio_año = hoy.replace(month=1, day=1)
    
    # Buscar presupuesto específico para cada período
    presupuesto_mes = PresupuestoMensual.objects.filter(
        vendedor=vendedor,
        año=hoy.year,
        mes=hoy.month,
        activo=True
    ).first()
    
    presupuesto_trimestre = PresupuestoMensual.objects.filter(
        vendedor=vendedor,
        año=inicio_trimestre.year,
        mes=inicio_trimestre.month,
        activo=True
    ).first()
    
    presupuesto_año = PresupuestoMensual.objects.filter(
        vendedor=vendedor,
        año=inicio_año.year,
        mes=inicio_año.month,
        activo=True
    ).first()
    
    # Presupuestos efectivos
    presupuesto_efectivo_mes = presupuesto_mes.monto_presupuesto if presupuesto_mes else vendedor.presupuesto
    presupuesto_efectivo_trimestre = presupuesto_trimestre.monto_presupuesto if presupuesto_trimestre else vendedor.presupuesto
    presupuesto_efectivo_año = presupuesto_año.monto_presupuesto if presupuesto_año else vendedor.presupuesto
    
    # Estadísticas del vendedor
    stats = {
        'mes': {
            'ventas': Pedido.objects.filter(
                vendedor=vendedor,
                fecha__gte=inicio_mes,
                estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
            ).aggregate(total=Sum('total'))['total'] or Decimal('0'),
            'pedidos': Pedido.objects.filter(
                vendedor=vendedor,
                fecha__gte=inicio_mes,
                estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
            ).count(),
        },
        'trimestre': {
            'ventas': Pedido.objects.filter(
                vendedor=vendedor,
                fecha__gte=inicio_trimestre,
                estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
            ).aggregate(total=Sum('total'))['total'] or Decimal('0'),
            'pedidos': Pedido.objects.filter(
                vendedor=vendedor,
                fecha__gte=inicio_trimestre,
                estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
            ).count(),
        },
        'año': {
            'ventas': Pedido.objects.filter(
                vendedor=vendedor,
                fecha__gte=inicio_año,
                estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
            ).aggregate(total=Sum('total'))['total'] or Decimal('0'),
            'pedidos': Pedido.objects.filter(
                vendedor=vendedor,
                fecha__gte=inicio_año,
                estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
            ).count(),
        }
    }
    
    # Productos más vendidos por este vendedor
    productos_vendedor = ItemPedido.objects.filter(
        pedido__vendedor=vendedor,
        pedido__fecha__gte=inicio_mes,
        pedido__estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).values(
        'producto__codigo',
        'producto__nombre'
    ).annotate(
        total_vendido=Sum('cantidad'),
        total_ingresos=Sum('subtotal')
    ).order_by('-total_vendido')[:10]
    
    # Clientes del vendedor
    clientes_vendedor = Pedido.objects.filter(
        vendedor=vendedor,
        fecha__gte=inicio_mes,
        estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).values(
        'cliente__id',
        'cliente__data'
    ).annotate(
        total_compras=Sum('total'),
        num_pedidos=Count('id')
    ).order_by('-total_compras')[:10]
    
    # Historial de seguimientos
    seguimientos = SeguimientoVendedor.objects.filter(
        vendedor=vendedor
    ).select_related('realizado_por').order_by('-fecha_seguimiento')[:10]
    
    # Mensajes enviados a este vendedor
    mensajes = MensajeJefeVentas.objects.filter(
        vendedor=vendedor
    ).order_by('-created_at')[:10]
    
    # Metas asignadas
    metas = MetaVendedor.objects.filter(
        vendedor=vendedor,
        activa=True
    ).order_by('-fecha_inicio')[:5]
    
    context = {
        'vendedor': vendedor,
        'stats': stats,
        'presupuesto_efectivo_mes': presupuesto_efectivo_mes,
        'presupuesto_efectivo_trimestre': presupuesto_efectivo_trimestre,
        'presupuesto_efectivo_año': presupuesto_efectivo_año,
        'productos_vendedor': productos_vendedor,
        'clientes_vendedor': clientes_vendedor,
        'seguimientos': seguimientos,
        'mensajes': mensajes,
        'metas': metas,
    }
    
    return render(request, 'usuarios/detalle_vendedor.html', context)

@user_passes_test(es_jefe_ventas, login_url='login')
@require_POST
def enviar_mensaje_vendedor(request):
    """Enviar mensaje a un vendedor específico"""
    try:
        data = json.loads(request.body)
        vendedor_id = data.get('vendedor_id')
        tipo = data.get('tipo', 'M')
        prioridad = data.get('prioridad', 'M')
        asunto = data.get('asunto')
        mensaje = data.get('mensaje')
        
        vendedor = get_object_or_404(Vendedor, id=vendedor_id)
        
        MensajeJefeVentas.objects.create(
            jefe=request.user,
            vendedor=vendedor,
            tipo=tipo,
            prioridad=prioridad,
            asunto=asunto,
            mensaje=mensaje
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Mensaje enviado correctamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al enviar mensaje: {str(e)}'
        })

@user_passes_test(es_jefe_ventas, login_url='login')
@require_POST
def asignar_meta_vendedor(request):
    """Asignar meta a un vendedor"""
    try:
        data = json.loads(request.body)
        vendedor_id = data.get('vendedor_id')
        tipo = data.get('tipo', 'M')
        monto_meta = Decimal(data.get('monto_meta'))
        fecha_inicio = datetime.strptime(data.get('fecha_inicio'), '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(data.get('fecha_fin'), '%Y-%m-%d').date()
        descripcion = data.get('descripcion', '')
        
        vendedor = get_object_or_404(Vendedor, id=vendedor_id)
        
        MetaVendedor.objects.create(
            vendedor=vendedor,
            asignada_por=request.user,
            tipo=tipo,
            monto_meta=monto_meta,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            descripcion=descripcion
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Meta asignada correctamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al asignar meta: {str(e)}'
        })

@user_passes_test(es_jefe_ventas, login_url='login')
@require_POST
def crear_seguimiento_vendedor(request):
    """Crear seguimiento para un vendedor"""
    try:
        data = json.loads(request.body)
        vendedor_id = data.get('vendedor_id')
        tipo = data.get('tipo', 'RE')
        fecha_seguimiento = datetime.strptime(data.get('fecha_seguimiento'), '%Y-%m-%d %H:%M')
        observaciones = data.get('observaciones')
        puntos_fuertes = data.get('puntos_fuertes', '')
        areas_mejora = data.get('areas_mejora', '')
        acciones_acordadas = data.get('acciones_acordadas', '')
        calificacion = data.get('calificacion')
        
        vendedor = get_object_or_404(Vendedor, id=vendedor_id)
        
        SeguimientoVendedor.objects.create(
            vendedor=vendedor,
            realizado_por=request.user,
            tipo=tipo,
            fecha_seguimiento=fecha_seguimiento,
            observaciones=observaciones,
            puntos_fuertes=puntos_fuertes,
            areas_mejora=areas_mejora,
            acciones_acordadas=acciones_acordadas,
            calificacion=int(calificacion) if calificacion else None
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Seguimiento creado correctamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al crear seguimiento: {str(e)}'
        })

@user_passes_test(es_jefe_ventas, login_url='login')
def reportes_equipo(request):
    """Generar reportes del equipo de ventas"""
    
    # Parámetros de filtro
    periodo = request.GET.get('periodo', 'mes')  # mes, trimestre, año
    vendedor_id = request.GET.get('vendedor_id')
    
    hoy = timezone.now().date()
    
    if periodo == 'trimestre':
        fecha_inicio = hoy.replace(month=((hoy.month-1)//3)*3+1, day=1)
    elif periodo == 'año':
        fecha_inicio = hoy.replace(month=1, day=1)
    else:  # mes
        fecha_inicio = hoy.replace(day=1)
    
    # Filtros base
    filtros = {
        'fecha__gte': fecha_inicio,
        'estado__in': [Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    }
    
    if vendedor_id:
        filtros['vendedor_id'] = vendedor_id
    
    # Datos del reporte
    pedidos = Pedido.objects.filter(**filtros).select_related('vendedor__user', 'cliente')
    
    # Resumen general
    resumen = {
        'total_ventas': pedidos.aggregate(total=Sum('total'))['total'] or Decimal('0'),
        'total_pedidos': pedidos.count(),
        'promedio_pedido': pedidos.aggregate(promedio=Avg('total'))['promedio'] or Decimal('0'),
        'vendedores_activos': pedidos.values('vendedor').distinct().count(),
    }
    
    # Desglose por vendedor
    vendedores_reporte = pedidos.values(
        'vendedor__user__first_name',
        'vendedor__user__last_name',
        'vendedor__presupuesto'
    ).annotate(
        total_ventas=Sum('total'),
        num_pedidos=Count('id'),
        promedio_pedido=Avg('total')
    ).order_by('-total_ventas')
    
    # Lista de vendedores para filtro
    todos_vendedores = Vendedor.objects.select_related('user').all()
    
    context = {
        'periodo': periodo,
        'vendedor_seleccionado': vendedor_id,
        'fecha_inicio': fecha_inicio,
        'resumen': resumen,
        'vendedores_reporte': vendedores_reporte,
        'todos_vendedores': todos_vendedores,
        'pedidos': pedidos[:50],  # Limitar para la vista
    }
    
    return render(request, 'usuarios/reportes_equipo.html', context)

@user_passes_test(es_jefe_ventas, login_url='login')
def mi_equipo(request):
    """Vista completa del equipo de vendedores para el jefe de ventas"""
    
    # Fechas para cálculos
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    hace_7_dias = hoy - timedelta(days=7)
    
    # Obtener solo los vendedores que pertenecen al grupo "Vendedor"
    vendedores_info = []
    
    for vendedor in Vendedor.objects.select_related('user').prefetch_related('user__profile', 'user__groups').filter(user__groups__name='Vendedor'):
        if not vendedor.user:
            continue
            
        # Estadísticas del vendedor
        # Ventas del mes actual
        ventas_mes = Pedido.objects.filter(
            vendedor=vendedor,
            fecha__gte=inicio_mes,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
        
        # Ventas de la semana
        ventas_semana = Pedido.objects.filter(
            vendedor=vendedor,
            fecha__gte=inicio_semana,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
        
        # Pedidos del mes
        pedidos_mes = Pedido.objects.filter(
            vendedor=vendedor,
            fecha__gte=inicio_mes,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).count()
        
        # Clientes únicos atendidos este mes
        clientes_mes = Cliente.objects.filter(
            pedido__vendedor=vendedor,
            pedido__fecha__gte=inicio_mes,
            pedido__estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).distinct().count()
        
        # Último pedido
        ultimo_pedido = Pedido.objects.filter(
            vendedor=vendedor,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).order_by('-fecha').first()
        
        # Días sin actividad
        dias_sin_actividad = (hoy - ultimo_pedido.fecha).days if ultimo_pedido else 999
        
        # Estado de actividad
        if dias_sin_actividad == 0:
            estado_actividad = 'activo_hoy'
            estado_texto = 'Activo hoy'
            estado_color = 'text-green-600'
            estado_bg = 'bg-green-100'
        elif dias_sin_actividad <= 3:
            estado_actividad = 'activo_reciente'
            estado_texto = f'Activo hace {dias_sin_actividad} día{"s" if dias_sin_actividad > 1 else ""}'
            estado_color = 'text-blue-600'
            estado_bg = 'bg-blue-100'
        elif dias_sin_actividad <= 7:
            estado_actividad = 'inactivo_reciente'
            estado_texto = f'Inactivo {dias_sin_actividad} días'
            estado_color = 'text-yellow-600'
            estado_bg = 'bg-yellow-100'
        else:
            estado_actividad = 'inactivo'
            estado_texto = f'Inactivo +{dias_sin_actividad} días'
            estado_color = 'text-red-600'
            estado_bg = 'bg-red-100'
        
        # Buscar presupuesto específico para el mes actual
        presupuesto_mes_actual = PresupuestoMensual.objects.filter(
            vendedor=vendedor,
            año=hoy.year,
            mes=hoy.month,
            activo=True
        ).first()
        
        # Usar presupuesto específico si existe, sino usar el presupuesto base
        presupuesto_efectivo = presupuesto_mes_actual.monto_presupuesto if presupuesto_mes_actual else vendedor.presupuesto
        
        # Porcentaje de cumplimiento de meta con el presupuesto efectivo
        porcentaje_meta = float((ventas_mes / presupuesto_efectivo * 100)) if presupuesto_efectivo > 0 else 0
        
        # Promedio por pedido
        promedio_pedido = float(ventas_mes / pedidos_mes) if pedidos_mes > 0 else 0
        
        # Mensajes no leídos del jefe
        mensajes_no_leidos = MensajeJefeVentas.objects.filter(
            vendedor=vendedor,
            jefe=request.user,
            leido=False
        ).count()
        
        # Metas activas
        metas_activas = MetaVendedor.objects.filter(
            vendedor=vendedor,
            activa=True,
            fecha_fin__gte=hoy
        ).count()
        
        # Último seguimiento
        ultimo_seguimiento = SeguimientoVendedor.objects.filter(
            vendedor=vendedor
        ).order_by('-fecha_seguimiento').first()
        
        # Información del perfil
        profile = getattr(vendedor.user, 'profile', None)
        
        vendedor_info = {
            'vendedor': vendedor,
            'user': vendedor.user,
            'profile': profile,
            'ventas_mes': ventas_mes,
            'ventas_semana': ventas_semana,
            'pedidos_mes': pedidos_mes,
            'clientes_mes': clientes_mes,
            'porcentaje_meta': porcentaje_meta,
            'presupuesto_efectivo': presupuesto_efectivo,
            'promedio_pedido': promedio_pedido,
            'dias_sin_actividad': dias_sin_actividad,
            'estado_actividad': estado_actividad,
            'estado_texto': estado_texto,
            'estado_color': estado_color,
            'estado_bg': estado_bg,
            'ultimo_pedido': ultimo_pedido,
            'mensajes_no_leidos': mensajes_no_leidos,
            'metas_activas': metas_activas,
            'ultimo_seguimiento': ultimo_seguimiento,
            'necesita_atencion': porcentaje_meta < 50 or dias_sin_actividad > 7,
        }
        
        vendedores_info.append(vendedor_info)
    
    # Ordenar por ventas del mes (descendente)
    vendedores_info.sort(key=lambda x: x['ventas_mes'], reverse=True)
    
    # Estadísticas generales del equipo
    total_vendedores = len(vendedores_info)
    vendedores_activos = len([v for v in vendedores_info if v['dias_sin_actividad'] <= 3])
    vendedores_necesitan_atencion = len([v for v in vendedores_info if v['necesita_atencion']])
    
    # Ventas totales del equipo
    ventas_totales_equipo = sum([v['ventas_mes'] for v in vendedores_info])
    
    # Calcular meta total del equipo usando presupuestos efectivos (mensuales específicos si existen)
    meta_total_equipo = Decimal('0')
    for v in vendedores_info:
        presupuesto_mes_actual = PresupuestoMensual.objects.filter(
            vendedor=v['vendedor'],
            año=hoy.year,
            mes=hoy.month,
            activo=True
        ).first()
        presupuesto_efectivo = presupuesto_mes_actual.monto_presupuesto if presupuesto_mes_actual else v['vendedor'].presupuesto
        meta_total_equipo += presupuesto_efectivo
    
    porcentaje_meta_equipo = float((ventas_totales_equipo / meta_total_equipo * 100)) if meta_total_equipo > 0 else 0
    
    # Filtros disponibles
    filtro_estado = request.GET.get('estado', 'todos')
    filtro_rendimiento = request.GET.get('rendimiento', 'todos')
    
    # Aplicar filtros
    vendedores_filtrados = vendedores_info.copy()
    
    if filtro_estado != 'todos':
        if filtro_estado == 'activos':
            vendedores_filtrados = [v for v in vendedores_filtrados if v['dias_sin_actividad'] <= 3]
        elif filtro_estado == 'inactivos':
            vendedores_filtrados = [v for v in vendedores_filtrados if v['dias_sin_actividad'] > 7]
    
    if filtro_rendimiento != 'todos':
        if filtro_rendimiento == 'alto':
            vendedores_filtrados = [v for v in vendedores_filtrados if v['porcentaje_meta'] >= 80]
        elif filtro_rendimiento == 'bajo':
            vendedores_filtrados = [v for v in vendedores_filtrados if v['porcentaje_meta'] < 50]
    
    context = {
        'vendedores_info': vendedores_filtrados,
        'total_vendedores': total_vendedores,
        'vendedores_activos': vendedores_activos,
        'vendedores_necesitan_atencion': vendedores_necesitan_atencion,
        'ventas_totales_equipo': ventas_totales_equipo,
        'meta_total_equipo': meta_total_equipo,
        'porcentaje_meta_equipo': porcentaje_meta_equipo,
        'filtro_estado': filtro_estado,
        'filtro_rendimiento': filtro_rendimiento,
        'fecha_actual': hoy,
    }
    
    return render(request, 'usuarios/mi_equipo.html', context)

@user_passes_test(es_jefe_ventas, login_url='login')
def presupuestos_metas(request):
    """Vista para gestionar presupuestos y metas del equipo de ventas"""
    
    # Fechas para cálculos
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    inicio_trimestre = hoy.replace(month=((hoy.month-1)//3)*3+1, day=1)
    inicio_año = hoy.replace(month=1, day=1)
    
    # Obtener todos los vendedores del grupo "Vendedor"
    vendedores_data = []
    
    for vendedor in Vendedor.objects.select_related('user').prefetch_related('user__groups').filter(user__groups__name='Vendedor'):
        if not vendedor.user:
            continue
            
        # Ventas actuales del mes
        ventas_mes = Pedido.objects.filter(
            vendedor=vendedor,
            fecha__gte=inicio_mes,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
        
        # Ventas del trimestre
        ventas_trimestre = Pedido.objects.filter(
            vendedor=vendedor,
            fecha__gte=inicio_trimestre,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
        
        # Ventas del año
        ventas_año = Pedido.objects.filter(
            vendedor=vendedor,
            fecha__gte=inicio_año,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
        
        # Porcentaje de cumplimiento del presupuesto mensual
        porcentaje_presupuesto = float((ventas_mes / vendedor.presupuesto * 100)) if vendedor.presupuesto > 0 else 0
        
        # Diferencia entre ventas y presupuesto (valor absoluto para mostrar)
        diferencia = abs(ventas_mes - vendedor.presupuesto)
        
        # Metas activas del vendedor
        metas_activas = MetaVendedor.objects.filter(
            vendedor=vendedor,
            activa=True,
            fecha_fin__gte=hoy
        ).order_by('fecha_fin')
        
        # Calcular progreso de cada meta
        metas_con_progreso = []
        for meta in metas_activas:
            progreso = meta.progreso_actual
            porcentaje = meta.porcentaje_cumplimiento
            
            # Determinar estado de la meta
            if porcentaje >= 100:
                estado_meta = 'completada'
                color_meta = 'text-green-600'
                bg_meta = 'bg-green-100'
            elif porcentaje >= 80:
                estado_meta = 'en_progreso_alto'
                color_meta = 'text-blue-600'
                bg_meta = 'bg-blue-100'
            elif porcentaje >= 50:
                estado_meta = 'en_progreso_medio'
                color_meta = 'text-yellow-600'
                bg_meta = 'bg-yellow-100'
            else:
                estado_meta = 'en_riesgo'
                color_meta = 'text-red-600'
                bg_meta = 'bg-red-100'
            
            # Días restantes
            dias_restantes = (meta.fecha_fin - hoy).days
            
            metas_con_progreso.append({
                'meta': meta,
                'progreso': progreso,
                'porcentaje': porcentaje,
                'estado': estado_meta,
                'color': color_meta,
                'bg': bg_meta,
                'dias_restantes': dias_restantes,
            })
        
        # Historial de metas completadas (últimas 5)
        metas_completadas = MetaVendedor.objects.filter(
            vendedor=vendedor,
            fecha_fin__lt=hoy
        ).order_by('-fecha_fin')[:5]
        
        vendedor_data = {
            'vendedor': vendedor,
            'user': vendedor.user,
            'presupuesto_mensual': vendedor.presupuesto,
            'ventas_mes': ventas_mes,
            'ventas_trimestre': ventas_trimestre,
            'ventas_año': ventas_año,
            'porcentaje_presupuesto': porcentaje_presupuesto,
            'diferencia': diferencia,
            'metas_activas': metas_con_progreso,
            'metas_completadas': metas_completadas,
            'total_metas_activas': len(metas_con_progreso),
        }
        
        vendedores_data.append(vendedor_data)
    
    # Ordenar por porcentaje de cumplimiento de presupuesto (descendente)
    vendedores_data.sort(key=lambda x: x['porcentaje_presupuesto'], reverse=True)
    
    # Estadísticas generales
    total_vendedores = len(vendedores_data)
    presupuesto_total_equipo = sum([v['presupuesto_mensual'] for v in vendedores_data])
    ventas_totales_equipo = sum([v['ventas_mes'] for v in vendedores_data])
    porcentaje_equipo = float((ventas_totales_equipo / presupuesto_total_equipo * 100)) if presupuesto_total_equipo > 0 else 0
    
    # Vendedores por estado de cumplimiento
    vendedores_excelentes = len([v for v in vendedores_data if v['porcentaje_presupuesto'] >= 100])
    vendedores_buenos = len([v for v in vendedores_data if 80 <= v['porcentaje_presupuesto'] < 100])
    vendedores_regulares = len([v for v in vendedores_data if 50 <= v['porcentaje_presupuesto'] < 80])
    vendedores_bajos = len([v for v in vendedores_data if v['porcentaje_presupuesto'] < 50])
    
    # Metas del equipo
    total_metas_activas = sum([v['total_metas_activas'] for v in vendedores_data])
    
    # Tipos de meta disponibles para el formulario
    tipos_meta = MetaVendedor.TipoMeta.choices
    
    context = {
        'vendedores_data': vendedores_data,
        'total_vendedores': total_vendedores,
        'presupuesto_total_equipo': presupuesto_total_equipo,
        'ventas_totales_equipo': ventas_totales_equipo,
        'porcentaje_equipo': porcentaje_equipo,
        'vendedores_excelentes': vendedores_excelentes,
        'vendedores_buenos': vendedores_buenos,
        'vendedores_regulares': vendedores_regulares,
        'vendedores_bajos': vendedores_bajos,
        'total_metas_activas': total_metas_activas,
        'tipos_meta': tipos_meta,
        'fecha_actual': hoy,
    }
    
    return render(request, 'usuarios/presupuestos_metas.html', context)

@user_passes_test(es_jefe_ventas, login_url='login')
@require_POST
def actualizar_presupuesto_vendedor(request):
    """Actualizar el presupuesto mensual de un vendedor"""
    try:
        data = json.loads(request.body)
        vendedor_id = data.get('vendedor_id')
        nuevo_presupuesto = Decimal(data.get('nuevo_presupuesto'))
        
        # Validar que el vendedor existe y pertenece al grupo correcto
        vendedor = get_object_or_404(
            Vendedor.objects.select_related('user').prefetch_related('user__groups'),
            id=vendedor_id,
            user__groups__name='Vendedor'
        )
        
        # Actualizar el presupuesto
        vendedor.presupuesto = nuevo_presupuesto
        vendedor.save()
        
        # Log de la acción
        logger.info(f"Presupuesto actualizado por {request.user.username}: Vendedor {vendedor.user.username} - Nuevo presupuesto: ${nuevo_presupuesto}")
        
        return JsonResponse({
            'success': True,
            'message': f'Presupuesto de {vendedor.user.get_full_name() or vendedor.user.username} actualizado a ${nuevo_presupuesto:,.0f}',
            'nuevo_presupuesto': float(nuevo_presupuesto),
            'vendedor_nombre': vendedor.user.get_full_name() or vendedor.user.username
        })
        
    except Vendedor.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Vendedor no encontrado o no tiene permisos para modificarlo'
        })
    except ValueError:
        return JsonResponse({
            'success': False,
            'message': 'El monto del presupuesto debe ser un número válido'
        })
    except Exception as e:
        logger.error(f"Error al actualizar presupuesto: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f'Error al actualizar presupuesto: {str(e)}'
        })

@user_passes_test(es_jefe_ventas, login_url='login')
@require_POST
def crear_presupuesto_mensual(request):
    """Crear o actualizar presupuesto mensual específico para un vendedor"""
    try:
        data = json.loads(request.body)
        vendedor_id = data.get('vendedor_id')
        año = int(data.get('año'))
        mes = int(data.get('mes'))
        monto_presupuesto = Decimal(data.get('monto_presupuesto'))
        observaciones = data.get('observaciones', '')
        
        # Validar que el vendedor existe y pertenece al grupo correcto
        vendedor = get_object_or_404(
            Vendedor.objects.select_related('user').prefetch_related('user__groups'),
            id=vendedor_id,
            user__groups__name='Vendedor'
        )
        
        # Crear o actualizar el presupuesto mensual
        presupuesto, created = PresupuestoMensual.objects.update_or_create(
            vendedor=vendedor,
            año=año,
            mes=mes,
            defaults={
                'monto_presupuesto': monto_presupuesto,
                'observaciones': observaciones,
                'asignado_por': request.user,
                'activo': True
            }
        )
        
        # Log de la acción
        accion = "creado" if created else "actualizado"
        logger.info(f"Presupuesto mensual {accion} por {request.user.username}: Vendedor {vendedor.user.username} - {presupuesto.get_mes_display()} {año}: ${monto_presupuesto}")
        
        return JsonResponse({
            'success': True,
            'message': f'Presupuesto de {vendedor.user.get_full_name() or vendedor.user.username} para {presupuesto.get_mes_display()} {año} {accion} correctamente',
            'presupuesto_id': presupuesto.id,
            'created': created
        })
        
    except Vendedor.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Vendedor no encontrado o no tiene permisos para modificarlo'
        })
    except ValueError as e:
        return JsonResponse({
            'success': False,
            'message': f'Datos inválidos: {str(e)}'
        })
    except Exception as e:
        logger.error(f"Error al crear/actualizar presupuesto mensual: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f'Error al procesar presupuesto: {str(e)}'
        })

@user_passes_test(es_jefe_ventas, login_url='login')
def presupuestos_mensuales(request):
    """Vista mejorada para gestionar presupuestos mensuales con historial"""
    
    # Parámetros de filtro
    año_seleccionado = int(request.GET.get('año', timezone.now().year))
    mes_seleccionado = int(request.GET.get('mes', timezone.now().month))
    
    # Fechas para cálculos
    hoy = timezone.now().date()
    fecha_seleccionada = hoy.replace(year=año_seleccionado, month=mes_seleccionado, day=1)
    
    # Obtener todos los vendedores del grupo "Vendedor"
    vendedores_data = []
    
    for vendedor in Vendedor.objects.select_related('user').prefetch_related('user__groups').filter(user__groups__name='Vendedor'):
        if not vendedor.user:
            continue
        
        # Buscar presupuesto específico para el mes seleccionado
        presupuesto_mes = PresupuestoMensual.objects.filter(
            vendedor=vendedor,
            año=año_seleccionado,
            mes=mes_seleccionado,
            activo=True
        ).first()
        
        # Si no hay presupuesto específico, usar el presupuesto base del vendedor
        monto_presupuesto = presupuesto_mes.monto_presupuesto if presupuesto_mes else vendedor.presupuesto
        
        # Calcular ventas para el mes seleccionado
        if mes_seleccionado == 12:
            fin_mes = fecha_seleccionada.replace(year=año_seleccionado + 1, month=1, day=1) - timedelta(days=1)
        else:
            fin_mes = fecha_seleccionada.replace(month=mes_seleccionado + 1, day=1) - timedelta(days=1)
        
        ventas_mes = Pedido.objects.filter(
            vendedor=vendedor,
            fecha__gte=fecha_seleccionada,
            fecha__lte=fin_mes,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
        
        # Calcular métricas
        porcentaje_cumplimiento = float((ventas_mes / monto_presupuesto * 100)) if monto_presupuesto > 0 else 0
        diferencia = ventas_mes - monto_presupuesto
        
        # Historial de presupuestos (últimos 6 meses)
        historial_presupuestos = []
        for i in range(6):
            fecha_hist = (fecha_seleccionada - timedelta(days=30*i)).replace(day=1)
            presupuesto_hist = PresupuestoMensual.objects.filter(
                vendedor=vendedor,
                año=fecha_hist.year,
                mes=fecha_hist.month,
                activo=True
            ).first()
            
            if presupuesto_hist:
                historial_presupuestos.append({
                    'fecha': fecha_hist,
                    'mes_nombre': fecha_hist.strftime('%B'),
                    'año': fecha_hist.year,
                    'monto': presupuesto_hist.monto_presupuesto,
                    'ventas_reales': presupuesto_hist.ventas_reales,
                    'porcentaje': presupuesto_hist.porcentaje_cumplimiento,
                    'observaciones': presupuesto_hist.observaciones
                })
        
        vendedor_data = {
            'vendedor': vendedor,
            'user': vendedor.user,
            'presupuesto_mes': presupuesto_mes,
            'monto_presupuesto': monto_presupuesto,
            'ventas_mes': ventas_mes,
            'porcentaje_cumplimiento': porcentaje_cumplimiento,
            'diferencia': abs(diferencia),
            'diferencia_positiva': diferencia >= 0,
            'historial_presupuestos': historial_presupuestos,
            'tiene_presupuesto_especifico': presupuesto_mes is not None,
        }
        
        vendedores_data.append(vendedor_data)
    
    # Ordenar por porcentaje de cumplimiento (descendente)
    vendedores_data.sort(key=lambda x: x['porcentaje_cumplimiento'], reverse=True)
    
    # Estadísticas generales
    total_vendedores = len(vendedores_data)
    presupuesto_total_mes = sum([v['monto_presupuesto'] for v in vendedores_data])
    ventas_totales_mes = sum([v['ventas_mes'] for v in vendedores_data])
    porcentaje_equipo = float((ventas_totales_mes / presupuesto_total_mes * 100)) if presupuesto_total_mes > 0 else 0
    
    # Vendedores por estado de cumplimiento
    vendedores_excelentes = len([v for v in vendedores_data if v['porcentaje_cumplimiento'] >= 100])
    vendedores_buenos = len([v for v in vendedores_data if 80 <= v['porcentaje_cumplimiento'] < 100])
    vendedores_regulares = len([v for v in vendedores_data if 50 <= v['porcentaje_cumplimiento'] < 80])
    vendedores_bajos = len([v for v in vendedores_data if v['porcentaje_cumplimiento'] < 50])
    
    # Opciones para los selectores
    años_disponibles = list(range(hoy.year - 2, hoy.year + 2))
    meses_disponibles = [
        (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
        (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
        (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
    ]
    
    context = {
        'vendedores_data': vendedores_data,
        'año_seleccionado': año_seleccionado,
        'mes_seleccionado': mes_seleccionado,
        'mes_nombre': fecha_seleccionada.strftime('%B'),
        'total_vendedores': total_vendedores,
        'presupuesto_total_mes': presupuesto_total_mes,
        'ventas_totales_mes': ventas_totales_mes,
        'porcentaje_equipo': porcentaje_equipo,
        'vendedores_excelentes': vendedores_excelentes,
        'vendedores_buenos': vendedores_buenos,
        'vendedores_regulares': vendedores_regulares,
        'vendedores_bajos': vendedores_bajos,
        'años_disponibles': años_disponibles,
        'meses_disponibles': meses_disponibles,
        'fecha_actual': hoy,
    }
    
    return render(request, 'usuarios/presupuestos_mensuales.html', context)

@user_passes_test(es_jefe_ventas, login_url='login')
def mensajes_equipo(request):
    """Vista para gestionar mensajes al equipo de ventas"""
    
    # Fechas para filtros
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    
    # Obtener todos los vendedores del grupo "Vendedor"
    vendedores = Vendedor.objects.select_related('user').prefetch_related('user__groups').filter(user__groups__name='Vendedor')
    
    # Filtros de la vista
    filtro_tipo = request.GET.get('tipo', 'todos')
    filtro_prioridad = request.GET.get('prioridad', 'todos')
    filtro_periodo = request.GET.get('periodo', 'mes')
    
    # Determinar fecha de inicio según el período
    if filtro_periodo == 'semana':
        fecha_inicio = hoy - timedelta(days=7)
    elif filtro_periodo == 'mes':
        fecha_inicio = inicio_mes
    elif filtro_periodo == 'trimestre':
        fecha_inicio = hoy.replace(month=((hoy.month-1)//3)*3+1, day=1)
    else:  # todos
        fecha_inicio = None
    
    # Consulta base de mensajes enviados por el jefe actual
    mensajes_query = MensajeJefeVentas.objects.filter(jefe=request.user).select_related('vendedor__user')
    
    # Aplicar filtros
    if fecha_inicio:
        mensajes_query = mensajes_query.filter(created_at__gte=fecha_inicio)
    
    if filtro_tipo != 'todos':
        mensajes_query = mensajes_query.filter(tipo=filtro_tipo)
    
    if filtro_prioridad != 'todos':
        mensajes_query = mensajes_query.filter(prioridad=filtro_prioridad)
    
    # Obtener mensajes ordenados por fecha
    mensajes = mensajes_query.order_by('-created_at')
    
    # Estadísticas de mensajes
    total_mensajes = mensajes.count()
    mensajes_no_leidos = mensajes.filter(leido=False).count()
    mensajes_leidos = mensajes.filter(leido=True).count()
    
    # Estadísticas por tipo
    stats_por_tipo = {}
    for tipo_key, tipo_label in MensajeJefeVentas.TipoMensaje.choices:
        count = mensajes.filter(tipo=tipo_key).count()
        stats_por_tipo[tipo_key] = {
            'label': tipo_label,
            'count': count,
            'porcentaje': (count / total_mensajes * 100) if total_mensajes > 0 else 0
        }
    
    # Estadísticas por prioridad
    stats_por_prioridad = {}
    for prioridad_key, prioridad_label in MensajeJefeVentas.Prioridad.choices:
        count = mensajes.filter(prioridad=prioridad_key).count()
        stats_por_prioridad[prioridad_key] = {
            'label': prioridad_label,
            'count': count,
            'porcentaje': (count / total_mensajes * 100) if total_mensajes > 0 else 0
        }
    
    # Vendedores con más mensajes recibidos
    vendedores_con_mensajes = mensajes.values(
        'vendedor__user__first_name',
        'vendedor__user__last_name',
        'vendedor__user__username',
        'vendedor__id'
    ).annotate(
        total_mensajes=Count('id'),
        mensajes_no_leidos=Count('id', filter=Q(leido=False)),
        ultimo_mensaje=Max('created_at')
    ).order_by('-total_mensajes')[:10]
    
    # Mensajes recientes (últimos 20)
    mensajes_recientes = mensajes[:20]
    
    # Preparar contexto
    context = {
        'vendedores': vendedores,
        'mensajes_recientes': mensajes_recientes,
        'total_mensajes': total_mensajes,
        'mensajes_no_leidos': mensajes_no_leidos,
        'mensajes_leidos': mensajes_leidos,
        'stats_por_tipo': stats_por_tipo,
        'stats_por_prioridad': stats_por_prioridad,
        'vendedores_con_mensajes': vendedores_con_mensajes,
        'filtro_tipo': filtro_tipo,
        'filtro_prioridad': filtro_prioridad,
        'filtro_periodo': filtro_periodo,
        'tipos_mensaje': MensajeJefeVentas.TipoMensaje.choices,
        'prioridades': MensajeJefeVentas.Prioridad.choices,
        'fecha_actual': hoy,
    }
    
    return render(request, 'usuarios/mensajes_equipo.html', context)

@user_passes_test(es_jefe_ventas, login_url='login')
@require_POST
def enviar_mensaje_grupal(request):
    """Enviar mensaje a múltiples vendedores o todo el equipo"""
    try:
        data = json.loads(request.body)
        destinatarios = data.get('destinatarios', [])  # Lista de IDs de vendedores
        enviar_a_todos = data.get('enviar_a_todos', False)
        tipo = data.get('tipo', 'M')
        prioridad = data.get('prioridad', 'M')
        asunto = data.get('asunto')
        mensaje = data.get('mensaje')
        
        # Validar datos requeridos
        if not asunto or not mensaje:
            return JsonResponse({
                'success': False,
                'message': 'El asunto y el mensaje son requeridos'
            })
        
        # Determinar destinatarios
        if enviar_a_todos:
            vendedores_destino = Vendedor.objects.filter(user__groups__name='Vendedor')
        else:
            if not destinatarios:
                return JsonResponse({
                    'success': False,
                    'message': 'Debe seleccionar al menos un destinatario'
                })
            vendedores_destino = Vendedor.objects.filter(
                id__in=destinatarios,
                user__groups__name='Vendedor'
            )
        
        # Crear mensajes para cada destinatario
        mensajes_creados = []
        for vendedor in vendedores_destino:
            mensaje_obj = MensajeJefeVentas.objects.create(
                jefe=request.user,
                vendedor=vendedor,
                tipo=tipo,
                prioridad=prioridad,
                asunto=asunto,
                mensaje=mensaje
            )
            mensajes_creados.append(mensaje_obj)
        
        # Log de la acción
        destinatarios_nombres = [v.user.get_full_name() or v.user.username for v in vendedores_destino]
        logger.info(f"Mensaje grupal enviado por {request.user.username}: '{asunto}' a {len(mensajes_creados)} vendedores: {', '.join(destinatarios_nombres)}")
        
        return JsonResponse({
            'success': True,
            'message': f'Mensaje enviado correctamente a {len(mensajes_creados)} vendedor{"es" if len(mensajes_creados) > 1 else ""}',
            'mensajes_enviados': len(mensajes_creados),
            'destinatarios': destinatarios_nombres
        })
        
    except Exception as e:
        logger.error(f"Error al enviar mensaje grupal: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f'Error al enviar mensaje: {str(e)}'
        })