#!/usr/bin/env python
"""
Script para probar el sistema de redirección de login
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpgestor20.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.test import Client
from django.urls import reverse

def setup_test_data():
    """Crear datos de prueba"""
    print("🔧 Configurando datos de prueba...")
    
    # Crear grupos si no existen
    grupos = ['Vendedor', 'JefeVentas', 'Gestor']
    for grupo_name in grupos:
        grupo, created = Group.objects.get_or_create(name=grupo_name)
        if created:
            print(f"✅ Grupo '{grupo_name}' creado")
        else:
            print(f"⚠️  Grupo '{grupo_name}' ya existe")
    
    # Crear usuarios de prueba
    usuarios_prueba = [
        {'username': 'vendedor1', 'password': 'test123', 'group': 'Vendedor'},
        {'username': 'jefe1', 'password': 'test123', 'group': 'JefeVentas'},
        {'username': 'gestor1', 'password': 'test123', 'group': 'Gestor'},
        {'username': 'sin_grupo', 'password': 'test123', 'group': None},
    ]
    
    for user_data in usuarios_prueba:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={'is_active': True}
        )
        
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"✅ Usuario '{user_data['username']}' creado")
        else:
            print(f"⚠️  Usuario '{user_data['username']}' ya existe")
        
        # Asignar grupo
        if user_data['group']:
            grupo = Group.objects.get(name=user_data['group'])
            user.groups.add(grupo)
            print(f"   → Asignado al grupo '{user_data['group']}'")

def test_login_redirects():
    """Probar las redirecciones de login"""
    print("\n🧪 PROBANDO REDIRECCIONES DE LOGIN")
    print("=" * 50)
    
    client = Client()
    
    # Casos de prueba
    test_cases = [
        {
            'username': 'vendedor1',
            'password': 'test123',
            'expected_redirect': '/dashboard/vendedor/',
            'description': 'Vendedor → Dashboard de Vendedor'
        },
        {
            'username': 'jefe1',
            'password': 'test123',
            'expected_redirect': '/dashboard/jefeventas/',
            'description': 'Jefe de Ventas → Dashboard de Jefe de Ventas'
        },
        {
            'username': 'gestor1',
            'password': 'test123',
            'expected_redirect': '/dashboard/gestor/',
            'description': 'Gestor → Dashboard de Gestión'
        },
        {
            'username': 'sin_grupo',
            'password': 'test123',
            'expected_redirect': '/dashboard/',
            'description': 'Sin grupo → Dashboard de redirección'
        }
    ]
    
    results = []
    
    for case in test_cases:
        print(f"\n🔍 Probando: {case['description']}")
        
        # Hacer login
        response = client.post('/accounts/login/', {
            'username': case['username'],
            'password': case['password']
        })
        
        # Verificar redirección
        if response.status_code == 302:  # Redirección exitosa
            redirect_url = response.url
            print(f"   ✅ Login exitoso")
            print(f"   🔗 Redirigido a: {redirect_url}")
            
            if case['expected_redirect'] in redirect_url:
                print(f"   ✅ Redirección correcta")
                results.append(True)
            else:
                print(f"   ❌ Redirección incorrecta")
                print(f"      Esperado: {case['expected_redirect']}")
                print(f"      Obtenido: {redirect_url}")
                results.append(False)
        else:
            print(f"   ❌ Login falló (código: {response.status_code})")
            results.append(False)
        
        # Logout para la siguiente prueba
        client.logout()
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS:")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    for i, (case, result) in enumerate(zip(test_cases, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {case['description']}")
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas de redirección pasaron!")
        return True
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa la configuración.")
        return False

def check_urls():
    """Verificar que las URLs estén configuradas correctamente"""
    print("\n🔍 VERIFICANDO URLS...")
    print("=" * 30)
    
    urls_to_check = [
        'login',
        'usuarios:dashboard_redirect',
        'usuarios:dashboard_vendedor',
        'usuarios:dashboard_jefeventas',
        'usuarios:dashboard_gestor',
    ]
    
    for url_name in urls_to_check:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name} → {url}")
        except Exception as e:
            print(f"❌ {url_name} → Error: {e}")

def main():
    """Función principal"""
    print("🧪 PRUEBA DEL SISTEMA DE REDIRECCIÓN DE LOGIN")
    print("=" * 60)
    
    try:
        # Verificar URLs
        check_urls()
        
        # Configurar datos de prueba
        setup_test_data()
        
        # Probar redirecciones
        success = test_login_redirects()
        
        print("\n💡 INSTRUCCIONES PARA USO MANUAL:")
        print("=" * 40)
        print("1. Ejecuta el servidor: python run_dev.py")
        print("2. Ve a: http://127.0.0.1:8000/accounts/login/")
        print("3. Prueba con estos usuarios:")
        print("   • vendedor1 / test123 → Dashboard de Vendedor")
        print("   • jefe1 / test123 → Dashboard de Jefe de Ventas")
        print("   • gestor1 / test123 → Dashboard de Gestión")
        print("   • sin_grupo / test123 → Redirección automática")
        
        return 0 if success else 1
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())