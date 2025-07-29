from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
import json

from .models import MensajeJefeVentas, Vendedor

@login_required
def inbox_mensajes(request):
    """Vista principal del inbox de mensajes para vendedores"""
    
    # Verificar que el usuario tenga un vendedor asociado
    try:
        vendedor = Vendedor.objects.get(user=request.user)
    except Vendedor.DoesNotExist:
        # Si es gestor o jefe de ventas, crear automáticamente un registro de Vendedor
        if request.user.groups.filter(name__in=['Gestor', 'JefeVentas']).exists():
            vendedor = Vendedor.objects.create(
                user=request.user,
                presupuesto=0
            )
        else:
            messages.error(request, 'No tienes permisos para acceder a los mensajes')
            return redirect('usuarios:dashboard_redirect')
    
    # Filtros
    filtro_tipo = request.GET.get('tipo', 'todos')
    filtro_prioridad = request.GET.get('prioridad', 'todos')
    filtro_estado = request.GET.get('estado', 'todos')
    busqueda = request.GET.get('busqueda', '')
    
    # Consulta base de mensajes recibidos
    mensajes_query = MensajeJefeVentas.objects.filter(
        vendedor=vendedor
    ).select_related('jefe')
    
    # Aplicar filtros
    if filtro_tipo != 'todos':
        mensajes_query = mensajes_query.filter(tipo=filtro_tipo)
    
    if filtro_prioridad != 'todos':
        mensajes_query = mensajes_query.filter(prioridad=filtro_prioridad)
    
    if filtro_estado == 'leidos':
        mensajes_query = mensajes_query.filter(leido=True)
    elif filtro_estado == 'no_leidos':
        mensajes_query = mensajes_query.filter(leido=False)
    
    if busqueda:
        mensajes_query = mensajes_query.filter(
            Q(asunto__icontains=busqueda) | 
            Q(mensaje__icontains=busqueda)
        )
    
    # Ordenar por fecha (más recientes primero)
    mensajes = mensajes_query.order_by('-created_at')
    
    # Paginación
    paginator = Paginator(mensajes, 10)
    page_number = request.GET.get('page')
    mensajes_page = paginator.get_page(page_number)
    
    # Estadísticas
    total_mensajes = mensajes_query.count()
    mensajes_no_leidos = mensajes_query.filter(leido=False).count()
    mensajes_leidos = mensajes_query.filter(leido=True).count()
    
    # Estadísticas por tipo
    stats_por_tipo = {}
    for tipo_key, tipo_label in MensajeJefeVentas.TipoMensaje.choices:
        count = mensajes_query.filter(tipo=tipo_key).count()
        stats_por_tipo[tipo_key] = {
            'label': tipo_label,
            'count': count,
            'porcentaje': (count / total_mensajes * 100) if total_mensajes > 0 else 0
        }
    
    # Estadísticas por prioridad
    stats_por_prioridad = {}
    for prioridad_key, prioridad_label in MensajeJefeVentas.Prioridad.choices:
        count = mensajes_query.filter(prioridad=prioridad_key).count()
        stats_por_prioridad[prioridad_key] = {
            'label': prioridad_label,
            'count': count,
            'porcentaje': (count / total_mensajes * 100) if total_mensajes > 0 else 0
        }
    
    context = {
        'mensajes': mensajes_page,
        'total_mensajes': total_mensajes,
        'mensajes_no_leidos': mensajes_no_leidos,
        'mensajes_leidos': mensajes_leidos,
        'stats_por_tipo': stats_por_tipo,
        'stats_por_prioridad': stats_por_prioridad,
        'filtro_tipo': filtro_tipo,
        'filtro_prioridad': filtro_prioridad,
        'filtro_estado': filtro_estado,
        'busqueda': busqueda,
        'tipos_mensaje': MensajeJefeVentas.TipoMensaje.choices,
        'prioridades': MensajeJefeVentas.Prioridad.choices,
    }
    
    return render(request, 'usuarios/inbox_mensajes.html', context)

@login_required
def detalle_mensaje(request, mensaje_id):
    """Vista para ver el detalle de un mensaje específico"""
    
    try:
        vendedor = Vendedor.objects.get(user=request.user)
    except Vendedor.DoesNotExist:
        messages.error(request, 'No tienes permisos para acceder a este mensaje')
        return redirect('usuarios:dashboard_redirect')
    
    mensaje = get_object_or_404(
        MensajeJefeVentas, 
        id=mensaje_id, 
        vendedor=vendedor
    )
    
    # Marcar como leído si no lo está
    if not mensaje.leido:
        mensaje.leido = True
        mensaje.fecha_leido = timezone.now()
        mensaje.save()
    
    # Obtener mensajes relacionados (del mismo jefe)
    mensajes_relacionados = MensajeJefeVentas.objects.filter(
        vendedor=vendedor,
        jefe=mensaje.jefe
    ).exclude(id=mensaje_id).order_by('-created_at')[:5]
    
    context = {
        'mensaje': mensaje,
        'mensajes_relacionados': mensajes_relacionados,
    }
    
    return render(request, 'usuarios/detalle_mensaje.html', context)

@login_required
@require_POST
def marcar_mensaje_leido(request, mensaje_id):
    """Marcar un mensaje como leído via AJAX"""
    
    try:
        vendedor = Vendedor.objects.get(user=request.user)
        mensaje = get_object_or_404(
            MensajeJefeVentas, 
            id=mensaje_id, 
            vendedor=vendedor
        )
        
        mensaje.leido = True
        mensaje.fecha_leido = timezone.now()
        mensaje.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Mensaje marcado como leído'
        })
        
    except Vendedor.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'No tienes permisos'
        }, status=403)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)

@login_required
@require_POST
def marcar_mensaje_no_leido(request, mensaje_id):
    """Marcar un mensaje como no leído via AJAX"""
    
    try:
        vendedor = Vendedor.objects.get(user=request.user)
        mensaje = get_object_or_404(
            MensajeJefeVentas, 
            id=mensaje_id, 
            vendedor=vendedor
        )
        
        mensaje.leido = False
        mensaje.fecha_leido = None
        mensaje.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Mensaje marcado como no leído'
        })
        
    except Vendedor.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'No tienes permisos'
        }, status=403)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)

@login_required
@require_POST
def marcar_todos_leidos(request):
    """Marcar todos los mensajes como leídos"""
    
    try:
        vendedor = Vendedor.objects.get(user=request.user)
        
        mensajes_actualizados = MensajeJefeVentas.objects.filter(
            vendedor=vendedor,
            leido=False
        ).update(
            leido=True,
            fecha_leido=timezone.now()
        )
        
        return JsonResponse({
            'success': True,
            'message': f'{mensajes_actualizados} mensajes marcados como leídos'
        })
        
    except Vendedor.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'No tienes permisos'
        }, status=403)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)

@login_required
def get_mensajes_count(request):
    """Obtener el conteo de mensajes no leídos para mostrar en el menú"""
    
    try:
        vendedor = Vendedor.objects.get(user=request.user)
        mensajes_no_leidos = MensajeJefeVentas.objects.filter(
            vendedor=vendedor,
            leido=False
        ).count()
        
        return JsonResponse({
            'success': True,
            'count': mensajes_no_leidos
        })
        
    except Vendedor.DoesNotExist:
        return JsonResponse({
            'success': True,
            'count': 0
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)