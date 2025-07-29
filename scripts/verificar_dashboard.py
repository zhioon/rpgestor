#!/usr/bin/env python
"""
Script para verificar que el dashboard de jefe de ventas funcione correctamente
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpgestor20.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User, Group
from usuarios.models import Vendedor
from django.urls import reverse

def verificar_dashboard():
    """Verificar que el dashboard funcione correctamente"""
    
    print("=== VERIFICACIÓN DEL DASHBOARD DE JEFE DE VENTAS ===")
    
    # Crear cliente de prueba
    client = Client()
    
    # Verificar que el usuario jefe_ventas existe
    try:
        jefe_user = User.objects.get(username='jefe_ventas')
        print("✓ Usuario jefe_ventas encontrado")
    except User.DoesNotExist:
        print("❌ Usuario jefe_ventas no encontrado")
        return False
    
    # Verificar que está en el grupo correcto
    jefe_ventas_group = Group.objects.get(name='JefeVentas')
    if jefe_user.groups.filter(name='JefeVentas').exists():
        print("✓ Usuario está en el grupo JefeVentas")
    else:
        print("❌ Usuario no está en el grupo JefeVentas")
        jefe_user.groups.add(jefe_ventas_group)
        print("✓ Usuario agregado al grupo JefeVentas")
    
    # Hacer login
    login_success = client.login(username='jefe_ventas', password='123456')
    if login_success:
        print("✓ Login exitoso")
    else:
        print("❌ Error en login")
        return False
    
    # Probar acceso al dashboard principal
    try:
        response = client.get(reverse('usuarios:dashboard_jefeventas_completo'))
        if response.status_code == 200:
            print("✓ Dashboard principal accesible")
        else:
            print(f"❌ Error en dashboard principal: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error al acceder al dashboard: {str(e)}")
        return False
    
    # Probar acceso a reportes
    try:
        response = client.get(reverse('usuarios:reportes_equipo'))
        if response.status_code == 200:
            print("✓ Reportes accesibles")
        else:
            print(f"❌ Error en reportes: {response.status_code}")
    except Exception as e:
        print(f"❌ Error al acceder a reportes: {str(e)}")
    
    # Probar acceso a detalle de vendedor (si existe algún vendedor)
    vendedores = Vendedor.objects.all()
    if vendedores.exists():
        try:
            vendedor = vendedores.first()
            response = client.get(reverse('usuarios:detalle_vendedor', args=[vendedor.id]))
            if response.status_code == 200:
                print("✓ Detalle de vendedor accesible")
            else:
                print(f"❌ Error en detalle de vendedor: {response.status_code}")
        except Exception as e:
            print(f"❌ Error al acceder a detalle de vendedor: {str(e)}")
    else:
        print("⚠️  No hay vendedores para probar detalle")
    
    print("\n=== VERIFICACIÓN DE URLS ===")
    urls_to_test = [
        'usuarios:dashboard_jefeventas_completo',
        'usuarios:reportes_equipo',
        'usuarios:enviar_mensaje_vendedor',
        'usuarios:asignar_meta_vendedor',
        'usuarios:crear_seguimiento_vendedor',
    ]
    
    for url_name in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✓ URL {url_name}: {url}")
        except Exception as e:
            print(f"❌ Error en URL {url_name}: {str(e)}")
    
    print("\n=== VERIFICACIÓN DE TEMPLATES ===")
    templates_to_check = [
        'usuarios/dashboard_jefeventas_completo.html',
        'usuarios/detalle_vendedor.html',
        'usuarios/reportes_equipo.html',
    ]
    
    for template in templates_to_check:
        template_path = os.path.join('usuarios', 'templates', template)
        if os.path.exists(template_path):
            print(f"✓ Template {template} existe")
        else:
            print(f"❌ Template {template} no encontrado")
    
    print("\n✅ Verificación completada")
    print("\nPuedes acceder al dashboard en:")
    print("URL: http://127.0.0.1:8000/usuarios/dashboard/jefeventas/completo/")
    print("Usuario: jefe_ventas")
    print("Contraseña: 123456")
    
    return True

if __name__ == '__main__':
    verificar_dashboard()