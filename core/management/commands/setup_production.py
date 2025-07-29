"""
Comando de Django para configurar el entorno de producción
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction


class Command(BaseCommand):
    help = 'Configura el entorno de producción con usuarios y grupos iniciales'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-superuser',
            action='store_true',
            help='Omitir creación de superusuario',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Iniciando configuración de producción...')
        )

        try:
            with transaction.atomic():
                # Crear grupos
                self.create_groups()
                
                # Crear superusuario si no se omite
                if not options['skip_superuser']:
                    self.create_superuser()
                
                # Crear usuarios demo
                self.create_demo_users()
                
                # Crear registros de vendedor
                self.create_vendedor_records()

            self.stdout.write(
                self.style.SUCCESS('🎉 Configuración completada exitosamente!')
            )
            
            self.show_credentials()

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error en configuración: {str(e)}')
            )
            raise

    def create_groups(self):
        """Crear grupos de usuarios"""
        self.stdout.write('📋 Creando grupos...')
        
        groups = ['Gestor', 'JefeVentas', 'Vendedor']
        
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'  ✅ Grupo "{group_name}" creado')
            else:
                self.stdout.write(f'  ℹ️ Grupo "{group_name}" ya existe')

    def create_superuser(self):
        """Crear superusuario"""
        self.stdout.write('👑 Creando superusuario...')
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@rpgestor.com',
                password='admin123'
            )
            self.stdout.write('  ✅ Superusuario "admin" creado')
        else:
            self.stdout.write('  ℹ️ Superusuario "admin" ya existe')

    def create_demo_users(self):
        """Crear usuarios de demostración"""
        self.stdout.write('👥 Creando usuarios demo...')
        
        demo_users = [
            {
                'username': 'gestor1',
                'email': 'gestor1@demo.com',
                'password': 'demo123',
                'first_name': 'María',
                'last_name': 'Gestora',
                'group': 'Gestor',
                'is_superuser': True
            },
            {
                'username': 'jefe1',
                'email': 'jefe1@demo.com',
                'password': 'demo123',
                'first_name': 'Carlos',
                'last_name': 'Jefe',
                'group': 'JefeVentas',
                'is_superuser': False
            },
            {
                'username': 'vendedor1',
                'email': 'vendedor1@demo.com',
                'password': 'demo123',
                'first_name': 'Juan',
                'last_name': 'Vendedor',
                'group': 'Vendedor',
                'is_superuser': False
            }
        ]
        
        for user_data in demo_users:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    is_staff=True,
                    is_active=True,
                    is_superuser=user_data['is_superuser']
                )
                
                # Asignar grupo
                try:
                    group = Group.objects.get(name=user_data['group'])
                    user.groups.add(group)
                    self.stdout.write(
                        f'  ✅ Usuario "{user_data["username"]}" creado y asignado al grupo "{user_data["group"]}"'
                    )
                except Group.DoesNotExist:
                    self.stdout.write(
                        f'  ⚠️ Grupo "{user_data["group"]}" no existe para usuario "{user_data["username"]}"'
                    )
            else:
                self.stdout.write(f'  ℹ️ Usuario "{user_data["username"]}" ya existe')

    def create_vendedor_records(self):
        """Crear registros de vendedor"""
        self.stdout.write('💼 Creando registros de vendedor...')
        
        try:
            from usuarios.models import Vendedor
            
            usernames = ['gestor1', 'jefe1', 'vendedor1']
            
            for username in usernames:
                try:
                    user = User.objects.get(username=username)
                    vendedor, created = Vendedor.objects.get_or_create(
                        user=user,
                        defaults={'presupuesto': 100000 if username == 'vendedor1' else 0}
                    )
                    
                    if created:
                        self.stdout.write(f'  ✅ Registro de vendedor creado para "{username}"')
                    else:
                        self.stdout.write(f'  ℹ️ Registro de vendedor ya existe para "{username}"')
                        
                except User.DoesNotExist:
                    self.stdout.write(f'  ⚠️ Usuario "{username}" no encontrado')
                    
        except ImportError:
            self.stdout.write('  ⚠️ Modelo Vendedor no disponible, omitiendo...')

    def show_credentials(self):
        """Mostrar credenciales disponibles"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('📋 CREDENCIALES DISPONIBLES:'))
        self.stdout.write('👔 Admin: admin / admin123')
        self.stdout.write('👔 Gestor: gestor1 / demo123')
        self.stdout.write('👨‍💼 Jefe: jefe1 / demo123')
        self.stdout.write('💼 Vendedor: vendedor1 / demo123')
        self.stdout.write('\n🌐 URLs:')
        self.stdout.write('📱 App: https://rpgestor.onrender.com')
        self.stdout.write('🔐 Admin: https://rpgestor.onrender.com/admin')
        self.stdout.write('='*50)