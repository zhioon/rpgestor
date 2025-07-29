import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

class AppConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"] is None or not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.user_id = self.scope['user'].id
        self.group_name = f"user_{self.user_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f'Conectado como usuario {self.user_id}'
        }))

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Handler para notificaciones de pedidos
    async def notify(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notificacion',
            **event["data"]
        }))

    # Handler para mensajes internos
    async def new_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'mensaje_interno',
            **event["data"]
        }))

    async def receive(self, text_data):
        # Opcional: manejar mensajes del cliente al servidor
        pass
