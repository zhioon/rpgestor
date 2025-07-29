from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from dateutil.relativedelta import relativedelta
import logging

logger = logging.getLogger(__name__)
logger.debug(f"Logger for {__name__} initialized.")

# Funciones de verificación de roles
def es_vendedor(user):
    return user.is_authenticated and user.groups.filter(name='Vendedor').exists()

def es_jefe_ventas(user):
    return user.is_authenticated and user.groups.filter(name='JefeVentas').exists()

def es_gestor(user):
    return user.is_authenticated and user.groups.filter(name='Gestor').exists()

# Dashboards con decoradores de seguridad
@user_passes_test(es_vendedor, login_url='login')
def dashboard_vendedor(request):
    """Dashboard específico para vendedores con datos reales"""
    logger.info(f"Acceso al dashboard de vendedor por usuario: {request.user.username}")
    
    from django.utils import timezone
    from django.db.models import Sum, Count, Q
    from datetime import datetime, timedelta
    from calendar import monthrange
    from .models import Vendedor
    from pedidos.models import Pedido, ItemPedido
    from productos.models import Producto
    from clientes.models import Cliente
    
    try:
        vendedor = Vendedor.objects.get(user=request.user)
    except Vendedor.DoesNotExist:
        messages.error(request, 'No se encontró información del vendedor')
        return redirect('login')
    
    # Fechas para cálculos
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    mes_anterior = (inicio_mes - timedelta(days=1)).replace(day=1)
    fin_mes_anterior = inicio_mes - timedelta(days=1)
    
    # === ESTADÍSTICAS PRINCIPALES ===
    
    # Ventas del mes actual
    pedidos_mes = Pedido.objects.filter(
        vendedor=vendedor,
        fecha__gte=inicio_mes,
        estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    )
    ventas_mes = pedidos_mes.aggregate(total=Sum('total'))['total'] or 0
    
    # Ventas del mes anterior para comparación
    pedidos_mes_anterior = Pedido.objects.filter(
        vendedor=vendedor,
        fecha__gte=mes_anterior,
        fecha__lte=fin_mes_anterior,
        estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    )
    ventas_mes_anterior = pedidos_mes_anterior.aggregate(total=Sum('total'))['total'] or 1
    
    # Cálculo de crecimiento
    crecimiento_ventas = ((ventas_mes - ventas_mes_anterior) / ventas_mes_anterior * 100) if ventas_mes_anterior > 0 else 0
    
    # Pedidos completados del mes
    pedidos_completados = pedidos_mes.count()
    pedidos_completados_anterior = pedidos_mes_anterior.count()
    crecimiento_pedidos = ((pedidos_completados - pedidos_completados_anterior) / pedidos_completados_anterior * 100) if pedidos_completados_anterior > 0 else 0
    
    # Clientes activos (con pedidos en los últimos 30 días)
    clientes_activos = Cliente.objects.filter(
        pedido__vendedor=vendedor,
        pedido__fecha__gte=hoy - timedelta(days=30)
    ).distinct().count()
    
    # Meta del mes
    from decimal import Decimal
    from .models import PresupuestoMensual # Importar PresupuestoMensual

    logger.info(f"Fecha actual para meta: {hoy}")
    meta_mes = Decimal('0')
    # Buscar el presupuesto mensual para el vendedor en el mes y año actuales
    presupuesto_mensual_obj = PresupuestoMensual.objects.filter(
        vendedor=vendedor,
        año=hoy.year,
        mes=hoy.month,
        activo=True,
    ).first() # Obtener el presupuesto mensual activo

    if presupuesto_mensual_obj:
        meta_mes = presupuesto_mensual_obj.monto_presupuesto
        logger.debug(f"PresupuestoMensual encontrado: ID={presupuesto_mensual_obj.id}, Monto={presupuesto_mensual_obj.monto_presupuesto}, Año={presupuesto_mensual_obj.año}, Mes={presupuesto_mensual_obj.mes}") # Changed to debug
    else:
        # Fallback a presupuesto base del vendedor si no hay presupuesto mensual específico
        meta_mes = vendedor.presupuesto if vendedor.presupuesto > 0 else Decimal('50000') # Valor por defecto si no hay presupuesto
        logger.info(f"No se encontró PresupuestoMensual. Usando presupuesto base del vendedor: {vendedor.presupuesto}")

    logger.info(f"Meta final del mes para {vendedor.user.username}: {meta_mes}")
    porcentaje_meta = float((ventas_mes / meta_mes * 100)) if meta_mes > 0 else 0
    
    # === PRODUCTOS MÁS VENDIDOS (SOLO PRODUCTOS ASIGNADOS) ===
    # Obtener productos asignados al vendedor a través de grupos y subgrupos
    productos_asignados = Producto.objects.filter(
        Q(grupo__in=vendedor.grupos.all()) | Q(subgrupo__in=vendedor.subgrupos.all())
    ).distinct()
    
    # Obtener productos top con objetos completos para acceder a las imágenes
    productos_vendidos = ItemPedido.objects.filter(
        pedido__vendedor=vendedor,
        pedido__fecha__gte=inicio_mes,
        pedido__estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO],
        producto__in=productos_asignados
    ).values('producto').annotate(
        total_vendido=Sum('cantidad'),
        total_ingresos=Sum('subtotal')
    ).order_by('-total_vendido')[:5]
    
    # Obtener los objetos de producto completos
    productos_top = []
    for item in productos_vendidos:
        producto = Producto.objects.get(id=item['producto'])
        productos_top.append({
            'producto': producto,
            'total_vendido': item['total_vendido'],
            'total_ingresos': item['total_ingresos']
        })
    
    # === CLIENTES CON MÁS VENTAS ===
    clientes_top = Pedido.objects.filter(
        vendedor=vendedor,
        fecha__gte=inicio_mes,
        estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).values(
        'cliente__id',
        'cliente__data'
    ).annotate(
        total_compras=Sum('total'),
        num_pedidos=Count('id')
    ).order_by('-total_compras')[:5]
    
    # === PEDIDOS RECIENTES ===
    pedidos_recientes = Pedido.objects.filter(
        vendedor=vendedor
    ).select_related('cliente').order_by('-created_at')[:10]
    
    # === DATOS PARA GRÁFICO DE PROGRESO DIARIO (MES ACTUAL) ===
    # Ventas acumuladas por día del mes actual
    dias_mes = monthrange(hoy.year, hoy.month)[1]
    ventas_diarias = []
    meta_mensual_linea = []
    labels_dias = []
    
    ventas_acumuladas = 0
    
    for dia in range(1, min(dias_mes + 1, hoy.day + 1)):
        fecha_dia = hoy.replace(day=dia)
        ventas_dia = Pedido.objects.filter(
            vendedor=vendedor,
            fecha=fecha_dia,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).aggregate(total=Sum('total'))['total'] or 0
        
        # Acumular ventas día a día
        ventas_acumuladas += float(ventas_dia)
        ventas_diarias.append(ventas_acumuladas)
        
        # Meta mensual como línea de referencia horizontal
        meta_mensual_linea.append(float(meta_mes))
        
        labels_dias.append(f"{dia}")
    
    context = {
        'user_role': 'Vendedor',
        'dashboard_title': 'Dashboard de Vendedor',
        'vendedor': vendedor,
        
        # Estadísticas principales
        'ventas_mes': ventas_mes,
        'crecimiento_ventas': round(crecimiento_ventas, 1),
        'pedidos_completados': pedidos_completados,
        'crecimiento_pedidos': round(crecimiento_pedidos, 1),
        'clientes_activos': clientes_activos,
        'meta_mes': meta_mes,
        'porcentaje_meta': round(porcentaje_meta, 1),
        
        # Listas
        'productos_top': productos_top,
        'clientes_top': clientes_top,
        'pedidos_recientes': pedidos_recientes,
        
        # Datos para gráfico diario
        'ventas_diarias': ventas_diarias,
        'metas_diarias': meta_mensual_linea,
        'labels_dias': labels_dias,
        'mes_actual': hoy.strftime('%B %Y'),
    }
    
    return render(request, 'usuarios/dashboard_vendedor.html', context)

@user_passes_test(es_jefe_ventas, login_url='login')
def dashboard_jefeventas(request):
    """Dashboard específico para jefes de ventas - Redirige al dashboard completo"""
    logger.info(f"Acceso al dashboard de jefe de ventas por usuario: {request.user.username}")
    
    # Redirigir al dashboard completo
    return redirect('usuarios:dashboard_jefeventas_completo')

@user_passes_test(es_gestor, login_url='login')
def dashboard_gestor(request):
    """Dashboard completo para gestores con todas las funcionalidades"""
    logger.info(f"Acceso al dashboard de gestor por usuario: {request.user}")
    logger.info(f"Is user authenticated: {request.user.is_authenticated}")
    
    from django.utils import timezone
    from django.db.models import Sum, Count, Q, Avg
    from datetime import datetime, timedelta
    from calendar import monthrange
    from decimal import Decimal
    from .models import Vendedor
    from pedidos.models import Pedido, ItemPedido
    from productos.models import Producto
    from clientes.models import Cliente
    from django.contrib.auth.models import User
    
    # Fechas para cálculos
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    mes_anterior = (inicio_mes - timedelta(days=1)).replace(day=1)
    fin_mes_anterior = inicio_mes - timedelta(days=1)
    
    # === ESTADÍSTICAS PRINCIPALES ===
    
    # Ventas totales del mes
    ventas_totales_mes = Pedido.objects.filter(
        fecha__gte=inicio_mes,
        estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).aggregate(total=Sum('total'))['total'] or Decimal('0')
    
    # Ventas del mes anterior para comparación
    ventas_mes_anterior = Pedido.objects.filter(
        fecha__gte=mes_anterior,
        fecha__lte=fin_mes_anterior,
        estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).aggregate(total=Sum('total'))['total'] or Decimal('1')
    
    # Crecimiento de ventas
    crecimiento_ventas = float(((ventas_totales_mes - ventas_mes_anterior) / ventas_mes_anterior * 100)) if ventas_mes_anterior and ventas_mes_anterior > 0 else 0
    
    # Meta total de todos los vendedores
    meta_total = Vendedor.objects.aggregate(total=Sum('presupuesto'))['total'] or Decimal('0')
    porcentaje_meta_total = float((ventas_totales_mes / meta_total * 100)) if meta_total and meta_total > 0 else 0
    
    # Pedidos totales del mes
    pedidos_totales_mes = Pedido.objects.filter(
        fecha__gte=inicio_mes,
        estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).count()
    
    # Pedidos del mes anterior
    pedidos_mes_anterior = Pedido.objects.filter(
        fecha__gte=mes_anterior,
        fecha__lte=fin_mes_anterior,
        estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).count()
    
    # Crecimiento de pedidos
    crecimiento_pedidos = ((pedidos_totales_mes - pedidos_mes_anterior) / pedidos_mes_anterior * 100) if pedidos_mes_anterior and pedidos_mes_anterior > 0 else 0
    
    # Vendedores activos este mes
    vendedores_activos = Vendedor.objects.filter(
        pedidos__fecha__gte=inicio_mes,
        pedidos__estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).distinct().count()
    
    # Total de vendedores
    total_vendedores = Vendedor.objects.count()
    
    # Clientes activos
    clientes_activos = Cliente.objects.filter(
        pedido__fecha__gte=inicio_mes,
        pedido__estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).distinct().count()
    
    # === RANKING DE VENDEDORES ===
    ranking_vendedores = Pedido.objects.filter(
        fecha__gte=inicio_mes,
        estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).values(
        'vendedor__user__first_name',
        'vendedor__user__last_name',
        'vendedor__user__username',
        'vendedor__presupuesto',
        'vendedor__id'
    ).annotate(
        total_ventas=Sum('total'),
        pedidos_count=Count('id')
    ).order_by('-total_ventas')[:10]
    
    # Calcular porcentaje de cumplimiento para cada vendedor
    for vendedor in ranking_vendedores:
        presupuesto = vendedor['vendedor__presupuesto']
        if presupuesto and presupuesto > 0:
            vendedor['porcentaje_cumplimiento'] = float((vendedor['total_ventas'] / presupuesto * 100))
        else:
            vendedor['porcentaje_cumplimiento'] = 0
    
    # === PRODUCTOS MÁS VENDIDOS GLOBALMENTE ===
    productos_mas_vendidos = ItemPedido.objects.filter(
        pedido__fecha__gte=inicio_mes,
        pedido__estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    ).values(
        'producto__codigo',
        'producto__nombre',
        'producto__imagen'
    ).annotate(
        total_vendido=Sum('cantidad'),
        total_ingresos=Sum('subtotal'),
        num_vendedores=Count('pedido__vendedor', distinct=True)
    ).order_by('-total_vendido')[:5]
    
    # === CLIENTES TOP GLOBALES ===
    clientes_top_global = Pedido.objects.filter(
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
    
    # === DATOS PARA GRÁFICO DE VENTAS DIARIAS GLOBALES ===
    dias_mes = monthrange(hoy.year, hoy.month)[1]
    ventas_diarias_global = []
    meta_mensual_linea = []
    labels_dias = []
    
    ventas_acumuladas = 0
    
    for dia in range(1, min(dias_mes + 1, hoy.day + 1)):
        fecha_dia = hoy.replace(day=dia)
        ventas_dia = Pedido.objects.filter(
            fecha=fecha_dia,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).aggregate(total=Sum('total'))['total'] or 0
        
        ventas_acumuladas += float(ventas_dia)
        ventas_diarias_global.append(ventas_acumuladas)
        meta_mensual_linea.append(float(meta_total))
        labels_dias.append(f"{dia}")
    
    # === PEDIDOS RECIENTES GLOBALES ===
    pedidos_recientes = Pedido.objects.select_related(
        'cliente', 'vendedor__user'
    ).order_by('-created_at')[:5]

    # Cálculos para Resumen Mensual
    dias_transcurridos = hoy.day
    promedio_ventas_dia = (ventas_totales_mes / dias_transcurridos) if dias_transcurridos > 0 else Decimal('0')
    mejor_vendedor = ranking_vendedores[0] if ranking_vendedores else None

    context = {
        'user': request.user,
        'user_role': 'Gestor',
        'dashboard_title': 'Dashboard de Gestión',
        
        # Estadísticas principales
        'ventas_totales_mes': ventas_totales_mes,
        'crecimiento_ventas': round(crecimiento_ventas, 1),
        'pedidos_totales_mes': pedidos_totales_mes,
        'crecimiento_pedidos': round(crecimiento_pedidos, 1),
        'vendedores_activos': vendedores_activos,
        'total_vendedores': total_vendedores,
        'clientes_activos': clientes_activos,
        
        # Rankings y tops
        'ranking_vendedores': ranking_vendedores,
        'productos_mas_vendidos': productos_mas_vendidos,
        'clientes_top_global': clientes_top_global,
        'pedidos_recientes': pedidos_recientes,
        
        # Datos para gráficos
        'ventas_diarias_global': ventas_diarias_global,
        'labels_dias': labels_dias,
        'mes_actual': hoy.strftime('%B %Y'),

        # Resumen Mensual
        'dias_transcurridos': dias_transcurridos,
        'promedio_ventas_dia': promedio_ventas_dia,
        'mejor_vendedor': mejor_vendedor,
    }
    
    return render(request, 'usuarios/dashboard_gestor.html', context)

# Vista adicional para manejar accesos no autorizados
@login_required
def dashboard_redirect(request):
    """
    Vista que redirige al dashboard apropiado según el rol del usuario
    Útil como fallback o para redirecciones manuales
    """
    user = request.user
    
    if es_vendedor(user):
        return redirect('usuarios:dashboard_vendedor')
    elif es_jefe_ventas(user):
        return redirect('usuarios:dashboard_jefeventas')
    elif es_gestor(user):
        return redirect('usuarios:dashboard_gestor')
    elif user.is_superuser:
        return redirect('admin:index')
    else:
        messages.error(request, 'No tienes permisos para acceder a ningún dashboard. Contacta al administrador.')
        return redirect('login')

