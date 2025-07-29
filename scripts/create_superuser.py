#!/usr/bin/env python
"""
Script para crear superusuario automáticamente en producción
"""
import os
import django
from django.core.management import execute_from_command_line

def create_superuser():
    """Crear superusuario automáticamente si no existe"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpgestor20.settings_production')
    django.setup()
    
    from django.contrib.auth.models import User
    
    # Crear o actualizar superusuario
    try:
        # Intentar obtener el usuario admin
        admin_user = User.objects.get(username='admin')
        # Si existe, actualizar la contraseña
        admin_user.set_password('rpgestor2025')
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
        print("✅ Superusuario actualizado: admin / rpgestor2025")
    except User.DoesNotExist:
        # Si no existe, crear nuevo superusuario
        User.objects.create_superuser(
            username='admin',
            email='admin@rpgestor.com',
            password='rpgestor2025'
        )
        print("✅ Superusuario creado: admin / rpgestor2025")
    
    # Crear superusuario alternativo
    try:
        alt_user = User.objects.get(username='gestor')
        alt_user.set_password('demo123')
        alt_user.is_superuser = True
        alt_user.is_staff = True
        alt_user.save()
        print("✅ Superusuario alternativo actualizado: gestor / demo123")
    except User.DoesNotExist:
        User.objects.create_superuser(
            username='gestor',
            email='gestor@rpgestor.com',
            password='demo123'
        )
        print("✅ Superusuario alternativo creado: gestor / demo123")

if __name__ == '__main__':
    create_superuser()