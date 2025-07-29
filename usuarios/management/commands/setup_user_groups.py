"""
Comando para crear los grupos de usuarios necesarios
Uso: python manage.py setup_user_groups
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Crea los grupos de usuarios necesarios para el sistema'

    def handle(self, *args, **options):
        # Definir los grupos que necesitamos
        grupos_necesarios = [
            {
                'name': 'Vendedor',
                'description': 'Usuarios vendedores con acceso limitado'
            },
            {
                'name': 'JefeVentas',
                'description': 'Jefes de ventas con permisos de supervisión'
            },
            {
                'name': 'Gestor',
                'description': 'Gestores con acceso completo al sistema'
            }
        ]

        self.stdout.write("🔧 Configurando grupos de usuarios...")
        self.stdout.write("=" * 50)

        for grupo_info in grupos_necesarios:
            grupo, created = Group.objects.get_or_create(
                name=grupo_info['name']
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Grupo '{grupo_info['name']}' creado exitosamente")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  Grupo '{grupo_info['name']}' ya existe")
                )

        # Verificar grupos existentes
        self.stdout.write("\n📋 Grupos disponibles en el sistema:")
        self.stdout.write("-" * 30)
        
        for grupo in Group.objects.all():
            usuarios_count = grupo.user_set.count()
            self.stdout.write(f"• {grupo.name} ({usuarios_count} usuarios)")

        self.stdout.write("\n💡 Para asignar usuarios a grupos:")
        self.stdout.write("   1. Ve al admin de Django (/admin/)")
        self.stdout.write("   2. Edita el usuario en 'Usuarios'")
        self.stdout.write("   3. Asigna el grupo correspondiente en 'Grupos'")
        
        self.stdout.write("\n🎉 Configuración de grupos completada!")
        
        return "Grupos configurados exitosamente"