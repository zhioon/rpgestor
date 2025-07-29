# notificaciones/signals.py

from django.db.models.signals import post_save
from django.dispatch        import receiver
from channels.layers        import get_channel_layer
from asgiref.sync           import async_to_sync

from pedidos.models         import Pedido
from usuarios.models        import Vendedor
from notificaciones.models  import Notification

@receiver(post_save, sender=Pedido)
def on_new_pedido(sender, instance, created, **kwargs):
    if not created:
        return

    layer = get_channel_layer()
    for vendedor in Vendedor.objects.select_related('user').all():
        # 1) Creamos la notificación en BD, asignando el user correcto
        notif = Notification.objects.create(
            user=vendedor.user,
            verb="Tienes un nuevo pedido",
            data={"pedido_id": instance.pk}
        )

        # 2) La enviamos al canal de ese usuario
        async_to_sync(layer.group_send)(
            f"user_{vendedor.user.id}",
            {
                "type": "notify",
                "data": {
                    "verb":      notif.verb,
                    "pedido_id": notif.data["pedido_id"],
                    "timestamp": str(notif.timestamp),
                }
            }
        )
