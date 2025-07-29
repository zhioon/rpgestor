import datetime
from django.shortcuts           import render
from django.http                import JsonResponse
from django.db.models           import Sum
from django.contrib.auth.decorators import login_required

from pedidos.models    import Pedido, ItemPedido
from productos.models  import Producto
from usuarios.models  import Vendedor 

@login_required
def dashboard(request):
    """
    Muestra la plantilla con todos los canvases de gráficos.
    """
    return render(request, 'insights/dashboard.html')


@login_required
def api_ventas(request):
    qs = Pedido.objects.filter(estado=Pedido.Estado.ENVIADO)
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')
    if desde:
        qs = qs.filter(fecha__gte=desde)
    if hasta:
        qs = qs.filter(fecha__lte=hasta)
    series = (
        qs.values('fecha')
          .annotate(total_ventas=Sum('total'))
          .order_by('fecha')
    )
    data = [
        {'fecha': x['fecha'].strftime('%Y-%m-%d'),
         'total': float(x['total_ventas'] or 0)}
        for x in series
    ]
    return JsonResponse({'ventas': data})


@login_required
def api_proyeccion(request):
    dias = int(request.GET.get('dias', 7))
    hoy = datetime.date.today()
    inicio = hoy - datetime.timedelta(days=30)
    ventas_qs = (
        Pedido.objects
              .filter(estado=Pedido.Estado.ENVIADO, fecha__gte=inicio)
              .values('fecha')
              .annotate(total=Sum('total'))
              .order_by('fecha')
    )
    ventas = {x['fecha']: float(x['total'] or 0) for x in ventas_qs}
    fechas = sorted(ventas.keys())
    proy = []
    for i in range(dias):
        window = fechas[-dias + i:] if len(fechas) >= dias else fechas
        valores = [ventas[d] for d in window]
        media = sum(valores)/len(valores) if valores else 0
        proy.append({
            'dia': (hoy + datetime.timedelta(days=i+1)).strftime('%Y-%m-%d'),
            'proyeccion': round(media, 2)
        })
    return JsonResponse({'proyeccion': proy})


@login_required
def api_ventas_por_vendedor(request):
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')
    qs = Pedido.objects.filter(estado=Pedido.Estado.ENVIADO)
    if desde:
        qs = qs.filter(fecha__gte=desde)
    if hasta:
        qs = qs.filter(fecha__lte=hasta)
    series = (
        qs.values('vendedor__user__username')
          .annotate(total_ventas=Sum('total'))
          .order_by('-total_ventas')
    )
    data = [
        {'vendedor': x['vendedor__user__username'], 'total': float(x['total_ventas'] or 0)}
        for x in series
    ]
    return JsonResponse({'ventas_vendedor': data})


@login_required
def api_ventas_por_producto(request):
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')
    qs = ItemPedido.objects.filter(pedido__estado=Pedido.Estado.ENVIADO)
    if desde:
        qs = qs.filter(pedido__fecha__gte=desde)
    if hasta:
        qs = qs.filter(pedido__fecha__lte=hasta)
    series = (
        qs.values('producto__nombre')
          .annotate(cantidad_vendida=Sum('cantidad'),
                    ingresos=Sum('subtotal'))
          .order_by('-ingresos')[:20]
    )
    data = [
        {
          'producto': x['producto__nombre'],
          'cantidad': int(x['cantidad_vendida'] or 0),
          'ingresos': float(x['ingresos'] or 0)
        }
        for x in series
    ]
    return JsonResponse({'ventas_producto': data})


@login_required
def api_ventas_por_grupo_subgrupo(request):
    """
    Agrupa ventas por grupo y subgrupo (productos agrupados) y devuelve el Top 5.
    GET params opcionales: desde, hasta (YYYY-MM-DD)
    """
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    qs = ItemPedido.objects.filter(pedido__estado=Pedido.Estado.ENVIADO)
    if desde:
        qs = qs.filter(pedido__fecha__gte=desde)
    if hasta:
        qs = qs.filter(pedido__fecha__lte=hasta)

    # TOP 5 grupos/subgrupos por ingresos
    series = (
        qs
        .values(
            'producto__subgrupo__grupo__nombre',
            'producto__subgrupo__nombre'
        )
        .annotate(ingresos=Sum('subtotal'))
        .order_by('-ingresos')[:5]
    )

    data = [
        {
            'grupo':    x['producto__subgrupo__grupo__nombre'],
            'subgrupo': x['producto__subgrupo__nombre'],
            'ingresos': float(x['ingresos'] or 0)
        }
        for x in series
    ]
    return JsonResponse({'ventas_grupo_subgrupo': data})

def api_ventas_por_grupo(request):
    """
    Agrupa las ventas por Grupo (p.ej. Sophia, Genfar, …) y devuelve el Top 5.
    Parámetros GET opcionales: desde, hasta (YYYY-MM-DD)
    """
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    # Solo ítems de pedidos confirmados
    qs = ItemPedido.objects.filter(pedido__estado=Pedido.Estado.ENVIADO)
    if desde:
        qs = qs.filter(pedido__fecha__gte=desde)
    if hasta:
        qs = qs.filter(pedido__fecha__lte=hasta)

    # Agrupamos por nombre de Grupo y sumamos subtotal de cada ítem
    series = (
        qs
        .values('producto__subgrupo__grupo__nombre')
        .annotate(ingresos=Sum('subtotal'))
        .order_by('-ingresos')[:5]    # Top 5 grupos
    )

    data = [
        {
            'grupo':   x['producto__subgrupo__grupo__nombre'],
            'ingresos': float(x['ingresos'] or 0),
        }
        for x in series
    ]
    return JsonResponse({'ventas_por_grupo': data})

@login_required
def api_ventas_diarias_vendedor(request):
    """Ventas diarias para el vendedor autenticado."""
    vendedor = Vendedor.objects.get(user=request.user)
    hoy = datetime.date.today()
    inicio = request.GET.get('desde', (hoy - datetime.timedelta(days=30)).isoformat())
    fin    = request.GET.get('hasta', hoy.isoformat())

    qs = Pedido.objects.filter(
        estado=Pedido.Estado.ENVIADO,
        vendedor=vendedor,
        fecha__range=[inicio, fin]
    )
    series = (
        qs.values('fecha')
          .annotate(total=Sum('total'))
          .order_by('fecha')
    )
    data = [{'fecha': x['fecha'].isoformat(), 'total': float(x['total'] or 0)} for x in series]
    return JsonResponse({'ventas_diarias': data})

@login_required
def api_top_productos_vendedor(request):
    """Top 5 productos más vendidos por el vendedor."""
    vendedor = Vendedor.objects.get(user=request.user)
    qs = ItemPedido.objects.filter(
        pedido__estado=Pedido.Estado.ENVIADO,
        pedido__vendedor=vendedor
    )
    series = (
        qs.values('producto__nombre')
          .annotate(cantidad=Sum('cantidad'))
          .order_by('-cantidad')[:5]
    )
    data = [{'producto': x['producto__nombre'], 'cantidad': int(x['cantidad'] or 0)} for x in series]
    return JsonResponse({'top_productos': data})

@login_required
def api_bottom_productos_vendedor(request):
    """Top 5 productos menos vendidos por el vendedor (pero vendidos)."""
    vendedor = Vendedor.objects.get(user=request.user)
    qs = ItemPedido.objects.filter(
        pedido__estado=Pedido.Estado.ENVIADO,
        pedido__vendedor=vendedor
    )
    series = (
        qs.values('producto__nombre')
          .annotate(cantidad=Sum('cantidad'))
          .order_by('cantidad')[:5]
    )
    data = [{'producto': x['producto__nombre'], 'cantidad': int(x['cantidad'] or 0)} for x in series]
    return JsonResponse({'bottom_productos': data})

@login_required
def api_presupuesto_vendedor(request):
    """Devuelve el presupuesto asignado al vendedor."""
    vendedor = Vendedor.objects.get(user=request.user)
    return JsonResponse({'presupuesto': float(vendedor.presupuesto)})