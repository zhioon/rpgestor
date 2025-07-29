#!/usr/bin/env python
"""
Script para probar una vista simple y aislar el problema
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpgestor20.settings')
django.setup()

from django.http import HttpResponse
from django.shortcuts import render
from django.test import Client
from django.contrib.auth.models import User

def test_simple_response():
    """Probar una respuesta HTTP simple"""
    
    print("=== PROBANDO RESPUESTA SIMPLE ===")
    
    # Crear cliente
    client = Client()
    
    # Login
    login_success = client.login(username='jefe_ventas', password='123456')
    if not login_success:
        print("❌ Error en login")
        return
    
    print("✓ Login exitoso")
    
    # Probar diferentes URLs para ver cuál funciona
    urls_to_test = [
        '/admin/',  # Esta debería funcionar
        '/usuarios/dashboard/',  # Dashboard redirect
        '/usuarios/dashboard/jefeventas/',  # Dashboard original
        '/usuarios/dashboard/jefeventas/completo/',  # Nuestro dashboard
        '/usuarios/dashboard/jefeventas/test/',  # Vista de prueba simple
    ]
    
    for url in urls_to_test:
        try:
            response = client.get(url)
            content = response.content.decode('utf-8')
            content_size = len(content)
            
            print(f"\n--- URL: {url} ---")
            print(f"Status: {response.status_code}")
            print(f"Content-Type: {response.get('Content-Type', 'No especificado')}")
            print(f"Tamaño: {content_size} caracteres")
            
            if content_size > 0:
                print(f"Primeros 100 chars: {repr(content[:100])}")
                print("✓ Esta URL devuelve contenido")
            else:
                print("❌ Esta URL devuelve contenido vacío")
                
        except Exception as e:
            print(f"❌ Error en {url}: {str(e)}")
    
    print(f"\n=== PROBANDO VISTA DIRECTA ===")
    
    # Probar llamar directamente a la vista
    try:
        from usuarios.jefe_ventas_views import dashboard_jefeventas_completo
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/test/')
        request.user = User.objects.get(username='jefe_ventas')
        
        # Llamar a la vista directamente
        response = dashboard_jefeventas_completo(request)
        
        print(f"✓ Vista ejecutada directamente")
        print(f"Status: {response.status_code}")
        print(f"Tipo de respuesta: {type(response)}")
        
        if hasattr(response, 'content'):
            content = response.content.decode('utf-8')
            print(f"Tamaño del contenido: {len(content)} caracteres")
            
            if len(content) > 0:
                print(f"Primeros 200 chars: {repr(content[:200])}")
            else:
                print("❌ Contenido vacío en respuesta directa")
        else:
            print("❌ La respuesta no tiene atributo 'content'")
            
    except Exception as e:
        print(f"❌ Error al llamar vista directamente: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_simple_response()