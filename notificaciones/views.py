# notificaciones/views.py
from django.shortcuts           import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls                import reverse
from channels.layers            import get_channel_layer
from asgiref.sync               import async_to_sync

from .models  import InternalMessage
from .forms   import InternalMessageForm

@login_required
def inbox(request):
    msgs = InternalMessage.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'notificaciones/inbox.html', {'msgs': msgs})

@login_required
def detalle_mensaje(request, pk):
    msg = get_object_or_404(InternalMessage, pk=pk, recipient=request.user)
    if not msg.read:
        msg.read = True
        msg.save(update_fields=['read'])
    return render(request, 'notificaciones/detalle_mensaje.html', {'msg': msg})

@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        form = InternalMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            # Notificar por WS al destinatario
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{msg.recipient.id}",  # Usar el grupo de usuario genérico
                {
                    "type": "new_message",  # El handler que debe ejecutarse en el consumer
                    "data": {
                        "sender": msg.sender.username,
                        "subject": msg.subject,
                        "url": reverse('notificaciones:detalle', kwargs={'pk': msg.pk}),
                        "timestamp": str(msg.timestamp),
                    }
                }
            )
            return redirect(reverse('notificaciones:inbox'))
    else:
        form = InternalMessageForm()
    return render(request, 'notificaciones/enviar_mensaje.html', {'form': form})

# Vista para probar WebSockets (sin requerir login para facilitar pruebas)
def test_websocket(request):
    return render(request, 'websocket_test.html')
