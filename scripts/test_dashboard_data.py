#!/usr/bin/env python
"""
Script para probar los datos que se pasan al dashboard
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpgestor20.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from usuarios.jefe_ventas_views import dashboard_jefeventas_completo
from django.test import RequestFactory

def test_dashboard_data():
    """Probar los datos que se generan para el dashboard"""
    
    print("=== PROBANDO DATOS DEL DASHBOARD ===")
    
    # Obtener usuario jefe de ventas
    try:
        jefe_user = User.objects.get(username='jefe_ventas')
        print(f"✓ Usuario encontrado: {jefe_user.username}")
    except User.DoesNotExist:
        print("❌ Usuario jefe_ventas no encontrado")
        return
    
    # Crear request simulado
    factory = RequestFactory()
    request = factory.get('/usuarios/dashboard/jefeventas/completo/')
    request.user = jefe_user
    
    try:
        # Llamar a la vista directamente
        response = dashboard_jefeventas_completo(request)
        print(f"✓ Vista ejecutada correctamente")
        print(f"✓ Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Dashboard cargado exitosamente")
            
            # El contexto no está directamente disponible en la respuesta,
            # pero podemos simular la lógica de la vista
            from django.utils import timezone
            from django.db.models import Sum, Count
            from datetime import timedelta
            from decimal import Decimal
            from usuarios.models import Vendedor
            from pedidos.models import Pedido
            
            # Fechas para cálculos
            hoy = timezone.now().date()
            inicio_mes = hoy.replace(day=1)
            
            # Estadísticas principales
            ventas_totales_mes = Pedido.objects.filter(
                fecha__gte=inicio_mes,
                estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
            ).aggregate(total=Sum('total'))['total'] or Decimal('0')
            
            pedidos_totales_mes = Pedido.objects.filter(
                fecha__gte=inicio_mes,
                estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
            ).count()
            
            total_vendedores = Vendedor.objects.count()
            
            print(f"\n=== DATOS CALCULADOS ===")
            print(f"✓ Ventas totales del mes: ${ventas_totales_mes:,.2f}")
            print(f"✓ Pedidos totales del mes: {pedidos_totales_mes}")
            print(f"✓ Total vendedores: {total_vendedores}")
            
            # Análisis de vendedores
            vendedores_con_datos = []
            for vendedor in Vendedor.objects.select_related('user').all():
                if not vendedor.user:
                    continue
                    
                ventas_mes = Pedido.objects.filter(
                    vendedor=vendedor,
                    fecha__gte=inicio_mes,
                    estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
                ).aggregate(total=Sum('total'))['total'] or Decimal('0')
                
                pedidos_mes = Pedido.objects.filter(
                    vendedor=vendedor,
                    fecha__gte=inicio_mes,
                    estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
                ).count()
                
                porcentaje_cumplimiento = float((ventas_mes / vendedor.presupuesto * 100)) if vendedor.presupuesto > 0 else 0
                
                vendedores_con_datos.append({
                    'nombre': f"{vendedor.user.first_name} {vendedor.user.last_name}",
                    'username': vendedor.user.username,
                    'ventas_mes': ventas_mes,
                    'pedidos_mes': pedidos_mes,
                    'presupuesto': vendedor.presupuesto,
                    'porcentaje_cumplimiento': porcentaje_cumplimiento
                })
            
            print(f"\n=== ANÁLISIS DE VENDEDORES ===")
            for vendedor_data in vendedores_con_datos:
                print(f"Vendedor: {vendedor_data['nombre']} ({vendedor_data['username']})")
                print(f"  - Ventas: ${vendedor_data['ventas_mes']:,.2f}")
                print(f"  - Pedidos: {vendedor_data['pedidos_mes']}")
                print(f"  - Meta: ${vendedor_data['presupuesto']:,.2f}")
                print(f"  - Cumplimiento: {vendedor_data['porcentaje_cumplimiento']:.1f}%")
                print()
            
            if len(vendedores_con_datos) == 0:
                print("⚠️  No hay vendedores con datos para mostrar")
            else:
                print(f"✓ {len(vendedores_con_datos)} vendedores con datos")
            
        else:
            print(f"❌ Error en la vista: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error al ejecutar la vista: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Probar también con el cliente de prueba
    print(f"\n=== PROBANDO CON CLIENTE HTTP ===")
    client = Client()
    
    # Login
    login_success = client.login(username='jefe_ventas', password='123456')
    if login_success:
        print("✓ Login exitoso")
        
        # Acceder al dashboard
        response = client.get('/usuarios/dashboard/jefeventas/completo/')
        print(f"✓ Response status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Mostrar los primeros 500 caracteres del contenido para debug
            print(f"\n=== CONTENIDO RECIBIDO (primeros 500 chars) ===")
            print(repr(content[:500]))
            
            # Verificar que el contenido tenga elementos esperados
            checks = [
                ('Dashboard de Jefe de Ventas', 'Título del dashboard'),
                ('FUNCIONANDO', 'Texto de prueba'),
                ('Ventas Totales', 'Estadísticas'),
                ('Equipo de Vendedores', 'Lista de vendedores'),
            ]
            
            print(f"\n=== VERIFICACIÓN DE CONTENIDO ===")
            for check, description in checks:
                if check in content:
                    print(f"✓ {description}: Encontrado")
                else:
                    print(f"❌ {description}: No encontrado")
            
            # Verificar tamaño del contenido
            content_size = len(content)
            print(f"\n✓ Tamaño del contenido: {content_size:,} caracteres")
            
            if content_size < 1000:
                print("⚠️  El contenido parece muy pequeño")
                if content_size > 0:
                    print(f"Contenido completo: {repr(content)}")
            else:
                print("✓ El contenido tiene un tamaño apropiado")
                
        else:
            print(f"❌ Error HTTP: {response.status_code}")
    else:
        print("❌ Error en login")
    
    print(f"\n✅ Prueba completada")
    print(f"\n🌐 Accede al dashboard en:")
    print(f"URL: http://127.0.0.1:8000/usuarios/dashboard/jefeventas/completo/")
    print(f"Usuario: jefe_ventas")
    print(f"Contraseña: 123456")

if __name__ == '__main__':
    test_dashboard_data()