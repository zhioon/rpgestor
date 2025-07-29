#!/usr/bin/env python
"""
Script de configuración para producción en Render
Ejecuta migraciones, crea superusuario y configura el sistema
"""

import os
import sys
import django
from pathlib import Path

# Agregar el directorio del proyecto al path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpgestor20.settings_production')

def setup_django():
    """Configurar Django"""
    try:
        django.setup()
        print("✅ Django configurado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error configurando Django: {e}")
        return False

def run_migrations():
    """Ejecutar migraciones de Django"""
    try:
        print("🔄 Ejecutando migraciones...")
        
        # Importar después de configurar Django
        from django.core.management import execute_from_command_line
        
        # Ejecutar migraciones
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✅ Migraciones ejecutadas correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error ejecutando migraciones: {e}")
        return False

def collect_static():
    """Recopilar archivos estáticos"""
    try:
        print("🔄 Recopilando archivos estáticos...")
        
        from django.core.management import execute_from_command_line
        
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Archivos estáticos recopilados")
        return True
        
    except Exception as e:
        print(f"❌ Error recopilando estáticos: {e}")
        return False

def create_superuser():
    """Crear superusuario automáticamente"""
    try:
        print("🔄 Creando superusuario...")
        
        from django.contrib.auth.models import User
        
        # Crear superusuario admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@rpgestor.com',
                password='admin123'
            )
            print("✅ Superusuario 'admin' creado")
        else:
            print("ℹ️ Superusuario 'admin' ya existe")
            
        # Crear usuario gestor
        if not User.objects.filter(username='gestor1').exists():
            User.objects.create_superuser(
                username='gestor1',
                email='gestor1@rpgestor.com',
                password='demo123'
            )
            print("✅ Usuario 'gestor1' creado")
        else:
            print("ℹ️ Usuario 'gestor1' ya existe")
            
        return True
        
    except Exception as e:
        print(f"❌ Error creando superusuario: {e}")
        return False

def create_groups():
    """Crear grupos de usuarios"""
    try:
        print("🔄 Creando grupos de usuarios...")
        
        from django.contrib.auth.models import Group
        
        groups = ['Gestor', 'JefeVentas', 'Vendedor']
        
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                print(f"✅ Grupo '{group_name}' creado")
            else:
                print(f"ℹ️ Grupo '{group_name}' ya existe")
                
        return True
        
    except Exception as e:
        print(f"❌ Error creando grupos: {e}")
        return False

def create_demo_users():
    """Crear usuarios de demostración"""
    try:
        print("🔄 Creando usuarios de demostración...")
        
        from django.contrib.auth.models import User, Group
        
        # Datos de usuarios demo
        demo_users = [
            {
                'username': 'jefe1',
                'email': 'jefe1@demo.com',
                'password': 'demo123',
                'first_name': 'Carlos',
                'last_name': 'Jefe',
                'group': 'JefeVentas'
            },
            {
                'username': 'vendedor1',
                'email': 'vendedor1@demo.com',
                'password': 'demo123',
                'first_name': 'Juan',
                'last_name': 'Vendedor',
                'group': 'Vendedor'
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
                    is_active=True
                )
                
                # Asignar grupo
                try:
                    group = Group.objects.get(name=user_data['group'])
                    user.groups.add(group)
                    print(f"✅ Usuario '{user_data['username']}' creado y asignado al grupo '{user_data['group']}'")
                except Group.DoesNotExist:
                    print(f"⚠️ Grupo '{user_data['group']}' no existe para usuario '{user_data['username']}'")
                    
            else:
                print(f"ℹ️ Usuario '{user_data['username']}' ya existe")
                
        return True
        
    except Exception as e:
        print(f"❌ Error creando usuarios demo: {e}")
        return False

def create_vendedor_records():
    """Crear registros de vendedor para los usuarios"""
    try:
        print("🔄 Creando registros de vendedor...")
        
        from django.contrib.auth.models import User
        from usuarios.models import Vendedor
        
        # Usuarios que necesitan registro de vendedor
        usernames = ['gestor1', 'jefe1', 'vendedor1']
        
        for username in usernames:
            try:
                user = User.objects.get(username=username)
                vendedor, created = Vendedor.objects.get_or_create(
                    user=user,
                    defaults={'presupuesto': 100000 if username == 'vendedor1' else 0}
                )
                
                if created:
                    print(f"✅ Registro de vendedor creado para '{username}'")
                else:
                    print(f"ℹ️ Registro de vendedor ya existe para '{username}'")
                    
            except User.DoesNotExist:
                print(f"⚠️ Usuario '{username}' no encontrado")
                
        return True
        
    except Exception as e:
        print(f"❌ Error creando registros de vendedor: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando configuración de producción...")
    print("=" * 50)
    
    # Paso 1: Configurar Django
    if not setup_django():
        sys.exit(1)
    
    # Paso 2: Ejecutar migraciones
    if not run_migrations():
        sys.exit(1)
    
    # Paso 3: Recopilar archivos estáticos
    if not collect_static():
        sys.exit(1)
    
    # Paso 4: Crear grupos
    if not create_groups():
        print("⚠️ Error creando grupos, continuando...")
    
    # Paso 5: Crear superusuario
    if not create_superuser():
        print("⚠️ Error creando superusuario, continuando...")
    
    # Paso 6: Crear usuarios demo
    if not create_demo_users():
        print("⚠️ Error creando usuarios demo, continuando...")
    
    # Paso 7: Crear registros de vendedor
    if not create_vendedor_records():
        print("⚠️ Error creando registros de vendedor, continuando...")
    
    print("=" * 50)
    print("🎉 Configuración de producción completada!")
    print("")
    print("📋 CREDENCIALES DISPONIBLES:")
    print("👔 Admin: admin / admin123")
    print("👔 Gestor: gestor1 / demo123")
    print("👨‍💼 Jefe: jefe1 / demo123")
    print("💼 Vendedor: vendedor1 / demo123")
    print("")
    print("🌐 URLs:")
    print("📱 App: https://rpgestor.onrender.com")
    print("🔐 Admin: https://rpgestor.onrender.com/admin")
    print("🛠️ Setup: https://rpgestor.onrender.com/setup-admin")

if __name__ == '__main__':
    main()