from django.core.management.base import BaseCommand
from notificaciones.models import InternalMessage

class Command(BaseCommand):
    help = 'Inspecciona el remitente y el destinatario del último mensaje interno creado.'

    def handle(self, *args, **options):
        last_message = InternalMessage.objects.order_by('-timestamp').first()

        if not last_message:
            self.stdout.write(self.style.WARNING('No se encontraron mensajes internos en la base de datos.'))
            return

        self.stdout.write(self.style.SUCCESS('--- Detalles del Último Mensaje Interno ---'))
        self.stdout.write(f'ID del Mensaje: {last_message.pk}')
        self.stdout.write(f'Fecha y Hora:    {last_message.timestamp}')
        self.stdout.write(f'Remitente (Sender):    {last_message.sender} (ID: {last_message.sender.pk})')
        self.stdout.write(f'Destinatario (Recipient): {last_message.recipient} (ID: {last_message.recipient.pk})')
        self.stdout.write(f'Asunto:          {last_message.subject}')
