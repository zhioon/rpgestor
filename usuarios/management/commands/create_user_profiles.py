from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from usuarios.models import UserProfile

class Command(BaseCommand):
    help = 'Crear perfiles para usuarios existentes que no tienen perfil'

    def handle(self, *args, **options):
        users_without_profile = User.objects.filter(profile__isnull=True)
        created_count = 0
        
        for user in users_without_profile:
            UserProfile.objects.create(user=user)
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Perfil creado para usuario: {user.username}')
            )
        
        if created_count == 0:
            self.stdout.write(
                self.style.WARNING('Todos los usuarios ya tienen perfil creado.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Se crearon {created_count} perfiles de usuario.')
            )