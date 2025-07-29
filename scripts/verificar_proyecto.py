#!/usr/bin/env python
"""
Script para verificar el estado del proyecto RPGestor
Útil para diagnosticar problemas en producción
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

def verificar_django():
    """Verificar configuración de Django"""
    try:
        django.setup()
        print("✅ Django configurado correctamente")
        
        from django.conf import settings
        print(f"✅ Base de datos: {settings.DATABASES['default']['ENGINE']}")
        print(f"✅ Debug mode: {settings.DEBUG}")
        print(f"✅ Allowed hosts: {settings.ALLOWED_HOSTS}")
        
        return True
    except Exception as e:
        print(f"❌ Error configurando Django: {e}")
        return False

def verificar_base_datos():
    """Verificar conexión a base de datos"""
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        print("✅ Conexión a base de datos exitosa")
        
        # Verificar tablas principales
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = [
            'auth_user',
            'auth_group',
            'usuarios_vendedor',
            'clientes_cliente',
            'productos_producto',
            'pedidos_pedido'
        ]
        
        missing_tables = []
        for table in required_tables:
            if table in tables:
                print(f"✅ Tabla '{table}' existe")
            else:
                print(f"❌ Tabla '{table}' NO existe")
                missing_tables.append(table)
        
        if missing_tables:
            print(f"⚠️ Faltan {len(missing_tables)} tablas. Ejecute migraciones.")
            return False
        else:
            print("✅ Todas las tablas requeridas existen")
            return True
            
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def verificar_usuarios():
    """Verificar usuarios del sistema"""
    try:
        from django.contrib.auth.models import User, Group
        
        # Verificar superusuarios
        superusers = User.objects.filter(is_superuser=True)
        print(f"✅ Superusuarios encontrados: {superusers.count()}")
        
        for user in superusers:
            print(f"  - {user.username} ({user.email})")
        
        # Verificar grupos
        groups = Group.objects.all()
        print(f"✅ Grupos encontrados: {groups.count()}")
        
        for group in groups:
            user_count = group.user_set.count()
            print(f"  - {group.name}: {user_count} usuarios")
        
        # Verificar usuarios demo
        demo_users = ['gestor1', 'jefe1', 'vendedor1']
        for username in demo_users:
            try:
                user = User.objects.get(username=username)
                groups_list = [g.name for g in user.groups.all()]
                print(f"✅ Usuario '{username}' existe - Grupos: {groups_list}")
            except User.DoesNotExist:
                print(f"❌ Usuario '{username}' NO existe")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando usuarios: {e}")
        return False

def verificar_vendedores():
    """Verificar registros de vendedor"""
    try:
        from usuarios.models import Vendedor
        
        vendedores = Vendedor.objects.all()
        print(f"✅ Registros de vendedor: {vendedores.count()}")
        
        for vendedor in vendedores:
            print(f"  - {vendedor.user.username}: ${vendedor.presupuesto}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando vendedores: {e}")
        return False

def verificar_datos_demo():
    """Verificar datos de demostración"""
    try:
        from clientes.models import Cliente
        from productos.models import Producto
        from pedidos.models import Pedido
        
        clientes_count = Cliente.objects.count()
        productos_count = Producto.objects.count()
        pedidos_count = Pedido.objects.count()
        
        print(f"✅ Clientes: {clientes_count}")
        print(f"✅ Productos: {productos_count}")
        print(f"✅ Pedidos: {pedidos_count}")
        
        if productos_count == 0:
            print("⚠️ No hay productos. Considere cargar datos de demostración.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando datos demo: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN DEL PROYECTO RPGESTOR")
    print("=" * 50)
    
    # Verificar Django
    print("\n📋 1. VERIFICANDO DJANGO...")
    if not verificar_django():
        print("❌ Fallo en verificación de Django")
        sys.exit(1)
    
    # Verificar base de datos
    print("\n📋 2. VERIFICANDO BASE DE DATOS...")
    if not verificar_base_datos():
        print("❌ Fallo en verificación de base de datos")
        print("💡 Solución: Ejecute 'python manage.py migrate'")
    
    # Verificar usuarios
    print("\n📋 3. VERIFICANDO USUARIOS...")
    if not verificar_usuarios():
        print("❌ Fallo en verificación de usuarios")
        print("💡 Solución: Ejecute el script de setup_production.py")
    
    # Verificar vendedores
    print("\n📋 4. VERIFICANDO VENDEDORES...")
    if not verificar_vendedores():
        print("❌ Fallo en verificación de vendedores")
    
    # Verificar datos demo
    print("\n📋 5. VERIFICANDO DATOS DEMO...")
    if not verificar_datos_demo():
        print("❌ Fallo en verificación de datos demo")
    
    print("\n" + "=" * 50)
    print("🎉 VERIFICACIÓN COMPLETADA")
    print("\n📞 Si hay problemas, contacte soporte técnico")

if __name__ == '__main__':
    main()