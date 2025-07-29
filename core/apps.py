from django.apps import AppConfig
import os


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        Ejecutar configuración inicial cuando Django esté listo
        Solo en producción y una sola vez
        """
        # Solo ejecutar en producción y si no es un comando de migración
        if (os.environ.get('DJANGO_SETTINGS_MODULE') == 'rpgestor20.settings_production' and 
            'migrate' not in os.sys.argv and 
            'collectstatic' not in os.sys.argv and
            'setup_production' not in os.sys.argv):
            
            # Importar aquí para evitar problemas de inicialización
            import threading
            import time
            
            def delayed_setup():
                """Configuración retrasada para asegurar que Django esté completamente listo"""
                time.sleep(3)  # Esperar 3 segundos
                try:
                    from django.contrib.auth.models import User, Group
                    from django.db import transaction
                    
                    with transaction.atomic():
                        # Crear grupos básicos si no existen
                        groups = ['Gestor', 'JefeVentas', 'Vendedor']
                        for group_name in groups:
                            Group.objects.get_or_create(name=group_name)
                        
                        # Crear superusuario básico si no existe
                        if not User.objects.filter(is_superuser=True).exists():
                            User.objects.create_superuser(
                                username='admin',
                                email='admin@rpgestor.com',
                                password='admin123'
                            )
                            print("✅ Superusuario de emergencia creado: admin / admin123")
                            
                except Exception as e:
                    print(f"⚠️ Setup automático falló (normal si ya está configurado): {e}")
            
            # Ejecutar en hilo separado para no bloquear el inicio
            threading.Thread(target=delayed_setup, daemon=True).start()