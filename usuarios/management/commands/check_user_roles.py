"""
Comando para verificar los roles de usuarios
Uso: python manage.py check_user_roles
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Verifica los roles asignados a los usuarios'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Verificar un usuario específico'
        )

    def handle(self, *args, **options):
        username = options.get('username')
        
        if username:
            # Verificar usuario específico
            try:
                user = User.objects.get(username=username)
                self.show_user_info(user)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"❌ Usuario '{username}' no encontrado")
                )
        else:
            # Mostrar todos los usuarios
            self.show_all_users()

    def show_user_info(self, user):
        """Muestra información detallada de un usuario"""
        self.stdout.write(f"\n👤 INFORMACIÓN DEL USUARIO: {user.username}")
        self.stdout.write("=" * 50)
        self.stdout.write(f"Nombre completo: {user.get_full_name() or 'No especificado'}")
        self.stdout.write(f"Email: {user.email or 'No especificado'}")
        self.stdout.write(f"Activo: {'✅ Sí' if user.is_active else '❌ No'}")
        self.stdout.write(f"Staff: {'✅ Sí' if user.is_staff else '❌ No'}")
        self.stdout.write(f"Superusuario: {'✅ Sí' if user.is_superuser else '❌ No'}")
        
        # Mostrar grupos
        grupos = user.groups.all()
        if grupos:
            self.stdout.write(f"\n🏷️  Grupos asignados:")
            for grupo in grupos:
                self.stdout.write(f"   • {grupo.name}")
        else:
            self.stdout.write(f"\n⚠️  Sin grupos asignados")
        
        # Determinar dashboard de redirección
        if user.groups.filter(name='Vendedor').exists():
            dashboard = "Dashboard de Vendedor"
        elif user.groups.filter(name='JefeVentas').exists():
            dashboard = "Dashboard de Jefe de Ventas"
        elif user.groups.filter(name='Gestor').exists():
            dashboard = "Dashboard de Gestión"
        elif user.is_superuser:
            dashboard = "Admin de Django"
        else:
            dashboard = "❌ Sin dashboard asignado"
        
        self.stdout.write(f"\n🎯 Dashboard de redirección: {dashboard}")

    def show_all_users(self):
        """Muestra resumen de todos los usuarios"""
        self.stdout.write("👥 RESUMEN DE USUARIOS Y ROLES")
        self.stdout.write("=" * 50)
        
        # Contar usuarios por grupo
        grupos_stats = {}
        for grupo in Group.objects.all():
            grupos_stats[grupo.name] = grupo.user_set.count()
        
        # Mostrar estadísticas
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        users_without_groups = User.objects.filter(groups__isnull=True).count()
        
        self.stdout.write(f"📊 Total de usuarios: {total_users}")
        self.stdout.write(f"✅ Usuarios activos: {active_users}")
        self.stdout.write(f"⚠️  Usuarios sin grupos: {users_without_groups}")
        
        self.stdout.write(f"\n🏷️  Usuarios por grupo:")
        for grupo_name, count in grupos_stats.items():
            self.stdout.write(f"   • {grupo_name}: {count} usuarios")
        
        # Mostrar usuarios sin grupos
        if users_without_groups > 0:
            self.stdout.write(f"\n⚠️  USUARIOS SIN GRUPOS ASIGNADOS:")
            users_no_groups = User.objects.filter(groups__isnull=True)
            for user in users_no_groups:
                status = "✅ Activo" if user.is_active else "❌ Inactivo"
                super_status = " (Superusuario)" if user.is_superuser else ""
                self.stdout.write(f"   • {user.username} - {status}{super_status}")
        
        # Mostrar todos los usuarios con sus grupos
        self.stdout.write(f"\n📋 DETALLE DE USUARIOS:")
        self.stdout.write("-" * 30)
        
        for user in User.objects.all().order_by('username'):
            grupos = [g.name for g in user.groups.all()]
            grupos_str = ", ".join(grupos) if grupos else "Sin grupos"
            status = "✅" if user.is_active else "❌"
            super_mark = "👑" if user.is_superuser else "👤"
            
            self.stdout.write(f"{super_mark} {user.username} {status} - {grupos_str}")
        
        self.stdout.write(f"\n💡 Para ver detalles de un usuario específico:")
        self.stdout.write(f"   python manage.py check_user_roles --username=NOMBRE_USUARIO")