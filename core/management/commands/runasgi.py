"""
Comando personalizado de Django para ejecutar el servidor ASGI
Uso: python manage.py runasgi
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import os
import sys

class Command(BaseCommand):
    help = 'Ejecuta el servidor ASGI con Channels para WebSockets'

    def add_arguments(self, parser):
        parser.add_argument(
            '--host',
            default=None,
            help='Host para el servidor (default: detecta automáticamente)'
        )
        parser.add_argument(
            '--port',
            type=int,
            default=8000,
            help='Puerto para el servidor (default: 8000)'
        )
        parser.add_argument(
            '--reload',
            action='store_true',
            help='Activar reload automático (solo para desarrollo)'
        )
        parser.add_argument(
            '--network',
            action='store_true',
            help='Permitir conexiones desde la red local (detecta IP automáticamente)'
        )
        parser.add_argument(
            '--localhost',
            action='store_true',
            help='Solo permitir conexiones locales (127.0.0.1)'
        )
        parser.add_argument(
            '--show-interfaces',
            action='store_true',
            help='Mostrar todas las interfaces de red disponibles'
        )

    def handle(self, *args, **options):
        try:
            from uvicorn import run
            from network_utils import get_local_ip, print_network_info, get_network_interfaces_summary, find_available_port
        except ImportError as e:
            if 'uvicorn' in str(e):
                self.stdout.write(
                    self.style.ERROR('❌ uvicorn no está instalado. Instálalo con: pip install uvicorn')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error importando dependencias: {e}')
                )
            sys.exit(1)

        # Mostrar interfaces si se solicita
        if options['show_interfaces']:
            get_network_interfaces_summary()
            return

        # Determinar host
        if options['host']:
            host = options['host']
        elif options['localhost']:
            host = "127.0.0.1"
        elif options['network']:
            host = "0.0.0.0"
        else:
            # Detectar automáticamente
            local_ip = get_local_ip()
            self.stdout.write("🚀 COMANDO DJANGO RUNASGI")
            self.stdout.write("=" * 50)
            self.stdout.write(f"🖥️  IP local detectada: {local_ip}")
            self.stdout.write("")
            self.stdout.write("¿Cómo quieres ejecutar el servidor?")
            self.stdout.write("1. 🏠 Solo en esta computadora (localhost)")
            self.stdout.write("2. 🌐 Accesible desde la red local")
            
            while True:
                try:
                    choice = input("\nElige una opción (1/2): ").strip()
                    if choice == "1":
                        host = "127.0.0.1"
                        break
                    elif choice == "2":
                        host = "0.0.0.0"
                        break
                    else:
                        self.stdout.write("❌ Opción inválida. Elige 1 o 2.")
                except KeyboardInterrupt:
                    self.stdout.write("\n👋 Cancelado por el usuario")
                    return

        port = options['port']
        reload = options['reload']

        # Verificar si el puerto está disponible
        if not find_available_port(host if host != "0.0.0.0" else "127.0.0.1", port, 1):
            self.stdout.write(f"⚠️  Puerto {port} no disponible, buscando alternativo...")
            alternative_port = find_available_port(host if host != "0.0.0.0" else "127.0.0.1", port + 1)
            if alternative_port:
                port = alternative_port
                self.stdout.write(f"✅ Usando puerto alternativo: {port}")
            else:
                self.stdout.write(
                    self.style.ERROR("❌ No se encontró un puerto disponible")
                )
                sys.exit(1)

        self.stdout.write("\n🚀 Iniciando servidor ASGI con Channels...")
        print_network_info(host, port)

        try:
            run(
                "rpgestor20.asgi:application",
                host=host,
                port=port,
                reload=reload,
                log_level="info",
                access_log=True
            )
        except KeyboardInterrupt:
            self.stdout.write("\n👋 Servidor detenido por el usuario")
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error al iniciar el servidor: {e}')
            )
            sys.exit(1)