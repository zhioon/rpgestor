from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages
from django.db import models
import json
from datetime import datetime, timedelta

from .models import EventoAgenda, Vendedor
from clientes.models import Cliente

@login_required
def mi_agenda(request):
    """Vista principal de la agenda del vendedor"""
    
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
            messages.error(request, 'No tienes permisos para acceder a la agenda')
            return redirect('usuarios:dashboard_redirect')
    
    # Obtener fecha actual y rango de fechas
    hoy = timezone.now().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    fin_semana = inicio_semana + timedelta(days=6)
    
    # Obtener eventos del vendedor
    eventos_hoy = EventoAgenda.objects.filter(
        vendedor=vendedor,
        fecha_inicio__date=hoy,
        estado__in=[EventoAgenda.Estado.PENDIENTE, EventoAgenda.Estado.EN_PROGRESO]
    ).order_by('fecha_inicio')
    
    eventos_semana = EventoAgenda.objects.filter(
        vendedor=vendedor,
        fecha_inicio__date__range=[inicio_semana, fin_semana]
    ).order_by('fecha_inicio')
    
    eventos_proximos = EventoAgenda.objects.filter(
        vendedor=vendedor,
        fecha_inicio__gte=timezone.now(),
        estado__in=[EventoAgenda.Estado.PENDIENTE, EventoAgenda.Estado.EN_PROGRESO]
    ).order_by('fecha_inicio')[:10]
    
    # Obtener clientes para el formulario con prioridad en favoritos
    from clientes.models import ClienteFavorito
    
    # 1. CLIENTES FAVORITOS (máxima prioridad)
    clientes_favoritos = Cliente.objects.filter(
        favorito_de__vendedor=vendedor
    ).distinct()
    
    # 2. CLIENTES RECIENTES (con pedidos en últimos 60 días)
    clientes_recientes = Cliente.objects.filter(
        pedido__vendedor=vendedor,
        pedido__created_at__gte=timezone.now() - timedelta(days=60)
    ).exclude(
        id__in=clientes_favoritos.values_list('id', flat=True)
    ).distinct()
    
    # 3. CLIENTES ACTIVOS (otros clientes con actividad reciente)
    clientes_activos = Cliente.objects.filter(
        pedido__created_at__gte=timezone.now() - timedelta(days=180)
    ).exclude(
        id__in=clientes_favoritos.values_list('id', flat=True)
    ).exclude(
        id__in=clientes_recientes.values_list('id', flat=True)
    ).distinct()
    
    # Combinar con prioridad: Favoritos + Recientes + Activos
    clientes = (
        list(clientes_favoritos[:20]) + 
        list(clientes_recientes[:40]) + 
        list(clientes_activos[:40])
    )
    
    # Estadísticas
    total_eventos = EventoAgenda.objects.filter(vendedor=vendedor).count()
    eventos_completados = EventoAgenda.objects.filter(
        vendedor=vendedor,
        estado=EventoAgenda.Estado.COMPLETADO
    ).count()
    eventos_pendientes = EventoAgenda.objects.filter(
        vendedor=vendedor,
        estado=EventoAgenda.Estado.PENDIENTE
    ).count()
    
    context = {
        'eventos_hoy': eventos_hoy,
        'eventos_semana': eventos_semana,
        'eventos_proximos': eventos_proximos,
        'clientes': clientes,
        'hoy': hoy,
        'inicio_semana': inicio_semana,
        'fin_semana': fin_semana,
        'estadisticas': {
            'total': total_eventos,
            'completados': eventos_completados,
            'pendientes': eventos_pendientes,
        }
    }
    
    return render(request, 'usuarios/mi_agenda.html', context)

@csrf_exempt
@login_required
def crear_evento_agenda(request):
    """Crear un nuevo evento en la agenda"""
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        vendedor = Vendedor.objects.get(user=request.user)
        data = json.loads(request.body)
        
        # Validar datos requeridos
        titulo = data.get('titulo', '').strip()
        fecha_inicio_str = data.get('fecha_inicio')
        
        if not titulo:
            return JsonResponse({'error': 'El título es requerido'}, status=400)
        
        if not fecha_inicio_str:
            return JsonResponse({'error': 'La fecha de inicio es requerida'}, status=400)
        
        # Convertir fecha
        try:
            fecha_inicio = datetime.fromisoformat(fecha_inicio_str.replace('Z', '+00:00'))
        except ValueError:
            return JsonResponse({'error': 'Formato de fecha inválido'}, status=400)
        
        # Crear evento
        evento = EventoAgenda.objects.create(
            vendedor=vendedor,
            titulo=titulo,
            descripcion=data.get('descripcion', ''),
            tipo=data.get('tipo', EventoAgenda.TipoEvento.VISITA),
            prioridad=data.get('prioridad', EventoAgenda.Prioridad.MEDIA),
            fecha_inicio=fecha_inicio,
            fecha_fin=datetime.fromisoformat(data.get('fecha_fin').replace('Z', '+00:00')) if data.get('fecha_fin') else None,
            cliente_id=data.get('cliente_id') if data.get('cliente_id') else None,
            ubicacion=data.get('ubicacion', ''),
            notas=data.get('notas', ''),
            minutos_recordatorio=int(data.get('minutos_recordatorio', 30))
        )
        
        return JsonResponse({
            'success': True,
            'evento': {
                'id': evento.id,
                'titulo': evento.titulo,
                'fecha_inicio': evento.fecha_inicio.isoformat(),
                'tipo': evento.get_tipo_display(),
                'prioridad': evento.get_prioridad_display(),
            }
        })
        
    except Vendedor.DoesNotExist:
        return JsonResponse({'error': 'No tienes permisos para crear eventos'}, status=403)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

@csrf_exempt
@login_required
def ajax_eventos_agenda(request):
    """Obtener eventos de la agenda para el calendario"""
    
    try:
        vendedor = Vendedor.objects.get(user=request.user)
        
        # Obtener parámetros de fecha
        start = request.GET.get('start')
        end = request.GET.get('end')
        
        if start and end:
            start_date = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_date = datetime.fromisoformat(end.replace('Z', '+00:00'))
            
            eventos = EventoAgenda.objects.filter(
                vendedor=vendedor,
                fecha_inicio__range=[start_date, end_date]
            )
        else:
            # Obtener eventos de los próximos 30 días
            eventos = EventoAgenda.objects.filter(
                vendedor=vendedor,
                fecha_inicio__gte=timezone.now(),
                fecha_inicio__lte=timezone.now() + timedelta(days=30)
            )
        
        # Formatear eventos para FullCalendar
        eventos_json = []
        for evento in eventos:
            color = {
                EventoAgenda.Prioridad.BAJA: '#6b7280',
                EventoAgenda.Prioridad.MEDIA: '#3b82f6',
                EventoAgenda.Prioridad.ALTA: '#f59e0b',
                EventoAgenda.Prioridad.URGENTE: '#ef4444',
            }.get(evento.prioridad, '#3b82f6')
            
            eventos_json.append({
                'id': evento.id,
                'title': evento.titulo,
                'start': evento.fecha_inicio.isoformat(),
                'end': evento.fecha_fin.isoformat() if evento.fecha_fin else None,
                'color': color,
                'extendedProps': {
                    'tipo': evento.get_tipo_display(),
                    'prioridad': evento.get_prioridad_display(),
                    'estado': evento.get_estado_display(),
                    'cliente': evento.cliente.data.get('Empresa', '') if evento.cliente else '',
                    'ubicacion': evento.ubicacion,
                    'descripcion': evento.descripcion,
                    'notas': evento.notas,
                }
            })
        
        return JsonResponse(eventos_json, safe=False)
        
    except Vendedor.DoesNotExist:
        return JsonResponse({'error': 'No tienes permisos'}, status=403)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@login_required
def ajax_buscar_clientes_agenda(request):
    """Búsqueda dinámica de clientes para la agenda"""
    
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        vendedor = Vendedor.objects.get(user=request.user)
        query = request.GET.get('q', '').strip()
        
        if len(query) < 2:
            return JsonResponse({'clientes': []})
        
        from clientes.models import ClienteFavorito
        
        # Buscar en diferentes campos
        clientes = Cliente.objects.filter(
            models.Q(data__Empresa__icontains=query) |
            models.Q(data__Razon_Comercial__icontains=query) |
            models.Q(data__Nit__icontains=query) |
            models.Q(data__Codigo__icontains=query)
        ).distinct()[:20]
        
        # Obtener IDs de clientes favoritos para marcarlos
        favoritos_ids = set(
            ClienteFavorito.objects.filter(vendedor=vendedor)
            .values_list('cliente_id', flat=True)
        )
        
        # Formatear resultados
        resultados = []
        for cliente in clientes:
            es_favorito = cliente.id in favoritos_ids
            
            resultados.append({
                'id': cliente.id,
                'empresa': cliente.data.get('Empresa', ''),
                'razon_comercial': cliente.data.get('Razon_Comercial', ''),
                'nit': cliente.data.get('Nit', ''),
                'codigo': cliente.data.get('Codigo', ''),
                'direccion': cliente.data.get('Direccion', ''),
                'es_favorito': es_favorito,
                'display_name': cliente.data.get('Empresa') or cliente.data.get('Razon_Comercial') or 'Cliente sin nombre'
            })
        
        # Ordenar: favoritos primero
        resultados.sort(key=lambda x: (not x['es_favorito'], x['display_name']))
        
        return JsonResponse({'clientes': resultados})
        
    except Vendedor.DoesNotExist:
        return JsonResponse({'error': 'No tienes permisos'}, status=403)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@login_required
def marcar_evento_completado(request, evento_id):
    """Marcar un evento como completado"""
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        vendedor = Vendedor.objects.get(user=request.user)
        evento = get_object_or_404(EventoAgenda, id=evento_id, vendedor=vendedor)
        
        evento.estado = EventoAgenda.Estado.COMPLETADO
        evento.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Evento marcado como completado'
        })
        
    except Vendedor.DoesNotExist:
        return JsonResponse({'error': 'No tienes permisos'}, status=403)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def crear_reunion(request):
    """Vista específica para crear reuniones"""
    
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
            messages.error(request, 'No tienes permisos para acceder a esta funcionalidad')
            return redirect('usuarios:dashboard_redirect')
    
    if request.method == 'POST':
        try:
            # Procesar datos del formulario
            titulo = request.POST.get('titulo', '').strip()
            descripcion = request.POST.get('descripcion', '').strip()
            fecha_inicio_str = request.POST.get('fecha_inicio')
            fecha_fin_str = request.POST.get('fecha_fin')
            vendedores_ids = request.POST.getlist('vendedores')
            ubicacion = request.POST.get('ubicacion', '').strip()
            prioridad = request.POST.get('prioridad', EventoAgenda.Prioridad.MEDIA)
            minutos_recordatorio = int(request.POST.get('minutos_recordatorio', 30))
            
            # Validaciones
            if not titulo:
                messages.error(request, 'El título de la reunión es requerido')
                return redirect('usuarios:crear_reunion')
            
            if not fecha_inicio_str:
                messages.error(request, 'La fecha y hora de inicio son requeridas')
                return redirect('usuarios:crear_reunion')
            
            if not vendedores_ids:
                messages.error(request, 'Debes seleccionar al menos un vendedor para la reunión')
                return redirect('usuarios:crear_reunion')
            
            # Convertir fechas
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%dT%H:%M')
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%dT%H:%M') if fecha_fin_str else None
            
            # Obtener vendedores seleccionados
            vendedores_seleccionados = Vendedor.objects.filter(id__in=vendedores_ids)
            
            if not vendedores_seleccionados.exists():
                messages.error(request, 'Los vendedores seleccionados no son válidos')
                return redirect('usuarios:crear_reunion')
            
            # Crear evento para cada vendedor seleccionado
            eventos_creados = []
            for vendedor_asignado in vendedores_seleccionados:
                evento = EventoAgenda.objects.create(
                    vendedor=vendedor_asignado,
                    titulo=titulo,
                    descripcion=descripcion,
                    tipo=EventoAgenda.TipoEvento.REUNION,
                    prioridad=prioridad,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    ubicacion=ubicacion,
                    minutos_recordatorio=minutos_recordatorio,
                    creado_por=request.user
                )
                eventos_creados.append(evento)
            
            # Agregar vendedores adicionales a cada evento (para referencia cruzada)
            for evento in eventos_creados:
                otros_vendedores = vendedores_seleccionados.exclude(id=evento.vendedor.id)
                evento.vendedores_adicionales.set(otros_vendedores)
            
            vendedores_nombres = [v.user.get_full_name() or v.user.username for v in vendedores_seleccionados]
            messages.success(request, f'Reunión "{titulo}" creada exitosamente para: {", ".join(vendedores_nombres)}')
            return redirect('usuarios:mi_agenda')
            
        except ValueError as e:
            messages.error(request, 'Error en el formato de fecha y hora')
            return redirect('usuarios:crear_reunion')
        except Exception as e:
            messages.error(request, f'Error al crear la reunión: {str(e)}')
            return redirect('usuarios:crear_reunion')
    
    # GET request - mostrar formulario
    # Obtener todos los vendedores para el formulario
    vendedores = Vendedor.objects.select_related('user').all().order_by('user__first_name', 'user__username')
    
    context = {
        'vendedores': vendedores,
        'prioridades': EventoAgenda.Prioridad.choices,
        'hoy': timezone.now().date(),
        'ahora': timezone.now().time(),
    }
    
    return render(request, 'usuarios/crear_reunion.html', context)

@login_required
def agendar_cita(request):
    """Vista específica para agendar citas con vendedores"""
    
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
            messages.error(request, 'No tienes permisos para acceder a esta funcionalidad')
            return redirect('usuarios:dashboard_redirect')
    
    if request.method == 'POST':
        try:
            # Procesar datos del formulario
            vendedor_id = request.POST.get('vendedor_id')
            titulo = request.POST.get('titulo', '').strip()
            fecha_inicio_str = request.POST.get('fecha_inicio')
            duracion_minutos = int(request.POST.get('duracion_minutos', 60))
            ubicacion = request.POST.get('ubicacion', '').strip()
            notas = request.POST.get('notas', '').strip()
            prioridad = request.POST.get('prioridad', EventoAgenda.Prioridad.MEDIA)
            minutos_recordatorio = int(request.POST.get('minutos_recordatorio', 30))
            
            # Validaciones
            if not vendedor_id:
                messages.error(request, 'Debes seleccionar un vendedor para la cita')
                return redirect('usuarios:agendar_cita')
            
            if not titulo:
                messages.error(request, 'El motivo de la cita es requerido')
                return redirect('usuarios:agendar_cita')
            
            if not fecha_inicio_str:
                messages.error(request, 'La fecha y hora de la cita son requeridas')
                return redirect('usuarios:agendar_cita')
            
            # Convertir fecha y calcular fecha fin
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%dT%H:%M')
            fecha_fin = fecha_inicio + timedelta(minutes=duracion_minutos)
            
            # Obtener vendedor asignado
            vendedor_asignado = get_object_or_404(Vendedor, id=vendedor_id)
            
            # Crear evento de cita
            evento = EventoAgenda.objects.create(
                vendedor=vendedor_asignado,
                titulo=f"Cita: {titulo}",
                descripcion=f"Cita programada por {request.user.get_full_name() or request.user.username}",
                tipo=EventoAgenda.TipoEvento.REUNION,  # Las citas individuales son reuniones
                prioridad=prioridad,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                ubicacion=ubicacion,
                notas=notas,
                minutos_recordatorio=minutos_recordatorio,
                creado_por=request.user
            )
            
            messages.success(request, f'Cita con {vendedor_asignado.user.get_full_name() or vendedor_asignado.user.username} agendada exitosamente')
            return redirect('usuarios:mi_agenda')
            
        except ValueError as e:
            messages.error(request, 'Error en el formato de fecha y hora')
            return redirect('usuarios:agendar_cita')
        except Exception as e:
            messages.error(request, f'Error al agendar la cita: {str(e)}')
            return redirect('usuarios:agendar_cita')
    
    # GET request - mostrar formulario
    # Obtener todos los vendedores para el formulario
    vendedores = Vendedor.objects.select_related('user').all().order_by('user__first_name', 'user__username')
    
    context = {
        'vendedores': vendedores,
        'prioridades': EventoAgenda.Prioridad.choices,
        'hoy': timezone.now().date(),
        'ahora': timezone.now().time(),
    }
    
    return render(request, 'usuarios/agendar_cita.html', context)

