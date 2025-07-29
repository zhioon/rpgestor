from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from notificaciones.models import InternalMessage
from django.utils import timezone

@login_required
def get_notifications(request):
    """API para obtener notificaciones del usuario"""
    # Obtener mensajes no leídos del usuario
    notifications = InternalMessage.objects.filter(
        recipient=request.user,
        read=False
    ).order_by('-timestamp')[:10]  # Últimas 10 notificaciones
    
    notifications_data = []
    for notification in notifications:
        notifications_data.append({
            'id': notification.id,
            'subject': notification.subject,
            'sender': notification.sender.get_full_name() or notification.sender.username,
            'timestamp': notification.timestamp.strftime('%d/%m/%Y %H:%M'),
            'body_preview': notification.body[:100] + '...' if len(notification.body) > 100 else notification.body,
            'url': f'/notificaciones/detalle/{notification.id}/'
        })
    
    return JsonResponse({
        'notifications': notifications_data,
        'count': len(notifications_data),
        'total_unread': InternalMessage.objects.filter(recipient=request.user, read=False).count()
    })

@login_required
def mark_notification_read(request, notification_id):
    """Marcar una notificación como leída"""
    if request.method == 'POST':
        try:
            notification = get_object_or_404(InternalMessage, id=notification_id, recipient=request.user)
            notification.read = True
            notification.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Notificación marcada como leída'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
def mark_all_notifications_read(request):
    """Marcar todas las notificaciones como leídas"""
    if request.method == 'POST':
        try:
            InternalMessage.objects.filter(recipient=request.user, read=False).update(read=True)
            
            return JsonResponse({
                'success': True,
                'message': 'Todas las notificaciones han sido marcadas como leídas'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
def get_notification_count(request):
    """Obtener el conteo de notificaciones no leídas"""
    count = InternalMessage.objects.filter(recipient=request.user, read=False).count()
    return JsonResponse({'count': count})