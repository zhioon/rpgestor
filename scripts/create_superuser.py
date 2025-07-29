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
    
    # Verificar si ya existe un superusuario
    if not User.objects.filter(is_superuser=True).exists():
        # Crear superusuario automáticamente
        User.objects.create_superuser(
            username='admin',
            email='admin@rpgestor.com',
            password='rpgestor2025'
        )
        print("✅ Superusuario creado: admin / rpgestor2025")
    else:
        print("✅ Superusuario ya existe")

if __name__ == '__main__':
    create_superuser()