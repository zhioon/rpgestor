from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Sum, Count, Q, Avg, F
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from calendar import monthrange
from decimal import Decimal
import json
import logging

from .models import Vendedor, MensajeJefeVentas, MetaVendedor, SeguimientoVendedor
from pedidos.models import Pedido, ItemPedido
from productos.models import Producto
from clientes.models import Cliente
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

def es_jefe_ventas(user):
    return user.is_authenticated and user.groups.filter(name='JefeVentas').exists()

@user_passes_test(es_jefe_ventas, login_url='login')
def dashboard_jefeventas_completo_simple(request):
    """Dashboard simplificado para debug"""
    
    try:
        logger.info("=== INICIANDO DASHBOARD SIMPLIFICADO ===")
        
        # Contexto mínimo
        context = {
            'ventas_totales_mes': 1000000,
            'pedidos_totales_mes': 50,
            'total_vendedores': 4,
        }
        
        logger.info(f"Contexto creado: {context}")
        
        # Intentar renderizar
        logger.info("Intentando renderizar template...")
        response = render(request, 'usuarios/dashboard_jefeventas.html', context)
        
        content_size = len(response.content)
        logger.info(f"Template renderizado. Tamaño: {content_size} bytes")
        
        if content_size == 0:
            logger.error("PROBLEMA: Template renderizado pero contenido vacío")
            return HttpResponse("""
                <h1>🚨 PROBLEMA IDENTIFICADO</h1>
                <p>El template se renderiza pero devuelve contenido vacío.</p>
                <p>Esto indica un problema en el template HTML.</p>
                <h2>Datos del contexto:</h2>
                <ul>
                    <li>Ventas: $1,000,000</li>
                    <li>Pedidos: 50</li>
                    <li>Vendedores: 4</li>
                </ul>
            """)
        
        return response
        
    except Exception as e:
        logger.error(f"ERROR EN DASHBOARD: {str(e)}")
        import traceback
        tb = traceback.format_exc()
        logger.error(f"Traceback completo: {tb}")
        
        return HttpResponse(f"""
            <h1>🚨 ERROR EN DASHBOARD</h1>
            <h2>Error:</h2>
            <p>{str(e)}</p>
            <h2>Traceback:</h2>
            <pre>{tb}</pre>
        """)