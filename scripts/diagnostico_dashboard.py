#!/usr/bin/env python
"""
Script de diagnóstico detallado para el dashboard de jefe de ventas
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpgestor20.settings')
django.setup()

from django.contrib.auth.models import User, Group
from usuarios.models import Vendedor
from pedidos.models import Pedido
from clientes.models import Cliente
from productos.models import Producto
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

def diagnostico_completo():
    """Diagnóstico completo del sistema"""
    
    print("=== DIAGNÓSTICO COMPLETO DEL DASHBOARD ===")
    
    # 1. Verificar usuarios y grupos
    print("\n1. USUARIOS Y GRUPOS:")
    try:
        jefe_user = User.objects.get(username='jefe_ventas')
        print(f"✓ Usuario jefe_ventas: {jefe_user.username}")
        print(f"  - Nombre: {jefe_user.first_name} {jefe_user.last_name}")
        print(f"  - Email: {jefe_user.email}")
        print(f"  - Activo: {jefe_user.is_active}")
        print(f"  - Staff: {jefe_user.is_staff}")
        
        grupos = jefe_user.groups.all()
        print(f"  - Grupos: {[g.name for g in grupos]}")
        
        if not jefe_user.groups.filter(name='JefeVentas').exists():
            print("❌ Usuario no está en el grupo JefeVentas")
            return False
        else:
            print("✓ Usuario está en el grupo JefeVentas")
            
    except User.DoesNotExist:
        print("❌ Usuario jefe_ventas no existe")
        return False
    
    # 2. Verificar vendedores
    print("\n2. VENDEDORES:")
    vendedores = Vendedor.objects.all()
    print(f"Total vendedores: {vendedores.count()}")
    
    for vendedor in vendedores:
        print(f"  - {vendedor.user.username}: {vendedor.user.first_name} {vendedor.user.last_name}")
        print(f"    Presupuesto: ${vendedor.presupuesto}")
        print(f"    Usuario asociado: {'✓' if vendedor.user else '❌'}")
    
    # 3. Verificar pedidos
    print("\n3. PEDIDOS:")
    pedidos_total = Pedido.objects.count()
    print(f"Total pedidos: {pedidos_total}")
    
    if pedidos_total > 0:
        # Pedidos por estado
        for estado in Pedido.Estado:
            count = Pedido.objects.filter(estado=estado.value).count()
            print(f"  - {estado.label}: {count}")
        
        # Pedidos con vendedor
        pedidos_con_vendedor = Pedido.objects.filter(vendedor__isnull=False).count()
        print(f"  - Con vendedor asignado: {pedidos_con_vendedor}")
        
        # Pedidos del mes actual
        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)
        pedidos_mes = Pedido.objects.filter(
            fecha__gte=inicio_mes,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).count()
        print(f"  - Finalizados este mes: {pedidos_mes}")
        
        # Pedidos recientes
        pedidos_recientes = Pedido.objects.order_by('-created_at')[:5]
        print("  - Últimos 5 pedidos:")
        for pedido in pedidos_recientes:
            vendedor_info = f"Vendedor: {pedido.vendedor.user.username}" if pedido.vendedor else "Sin vendedor"
            print(f"    #{pedido.id} - ${pedido.total} - {pedido.get_estado_display()} - {vendedor_info}")
    
    # 4. Verificar clientes
    print("\n4. CLIENTES:")
    clientes_total = Cliente.objects.count()
    print(f"Total clientes: {clientes_total}")
    
    # 5. Verificar productos
    print("\n5. PRODUCTOS:")
    productos_total = Producto.objects.count()
    print(f"Total productos: {productos_total}")
    
    # 6. Simular datos de la vista
    print("\n6. SIMULACIÓN DE DATOS DE LA VISTA:")
    try:
        from usuarios.jefe_ventas_views import dashboard_jefeventas_completo
        from django.test import RequestFactory
        from django.contrib.auth.models import AnonymousUser
        
        # Crear request simulado
        factory = RequestFactory()
        request = factory.get('/usuarios/dashboard/jefeventas/completo/')
        request.user = jefe_user
        
        print("✓ Request simulado creado")
        print("✓ Usuario asignado al request")
        
        # Verificar datos que la vista debería generar
        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)
        
        # Ventas del mes
        ventas_mes = Pedido.objects.filter(
            fecha__gte=inicio_mes,
            estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
        ).count()
        print(f"✓ Ventas del mes para la vista: {ventas_mes}")
        
        # Vendedores para análisis
        vendedores_para_analisis = Vendedor.objects.select_related('user').all()
        print(f"✓ Vendedores para análisis: {vendedores_para_analisis.count()}")
        
        # Verificar que todos los vendedores tienen usuario
        vendedores_sin_usuario = [v for v in vendedores_para_analisis if not v.user]
        if vendedores_sin_usuario:
            print(f"❌ Vendedores sin usuario: {len(vendedores_sin_usuario)}")
        else:
            print("✓ Todos los vendedores tienen usuario asociado")
            
    except Exception as e:
        print(f"❌ Error en simulación de vista: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # 7. Verificar template
    print("\n7. TEMPLATE:")
    template_path = 'usuarios/templates/usuarios/dashboard_jefeventas_completo.html'
    if os.path.exists(template_path):
        print("✓ Template existe")
        
        # Verificar tamaño del archivo
        size = os.path.getsize(template_path)
        print(f"✓ Tamaño del template: {size} bytes")
        
        if size < 1000:
            print("⚠️  Template parece muy pequeño")
        
        # Verificar contenido básico
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '{% extends' in content:
            print("✓ Template extiende correctamente")
        else:
            print("❌ Template no extiende base")
            
        if '{% block content %}' in content:
            print("✓ Bloque content encontrado")
        else:
            print("❌ Bloque content no encontrado")
            
        if 'vendedores_detalle' in content:
            print("✓ Variable vendedores_detalle encontrada en template")
        else:
            print("❌ Variable vendedores_detalle no encontrada")
            
    else:
        print("❌ Template no existe")
    
    # 8. Verificar URLs
    print("\n8. URLS:")
    try:
        from django.urls import reverse
        url = reverse('usuarios:dashboard_jefeventas_completo')
        print(f"✓ URL dashboard: {url}")
    except Exception as e:
        print(f"❌ Error en URL: {str(e)}")
    
    print("\n=== RESUMEN ===")
    if pedidos_total == 0:
        print("⚠️  NO HAY PEDIDOS - El dashboard estará vacío")
        print("   Solución: Crear algunos pedidos de prueba")
    
    if vendedores.count() == 0:
        print("⚠️  NO HAY VENDEDORES - El dashboard estará vacío")
        print("   Solución: Crear algunos vendedores de prueba")
    
    print("\n✅ Diagnóstico completado")
    return True

def crear_datos_prueba_completos():
    """Crear datos de prueba más completos"""
    print("\n=== CREANDO DATOS DE PRUEBA COMPLETOS ===")
    
    from django.utils import timezone
    from datetime import datetime, timedelta
    import random
    
    # Crear algunos pedidos de prueba
    vendedores = Vendedor.objects.all()
    clientes = Cliente.objects.all()[:5]  # Usar solo los primeros 5 clientes
    
    if vendedores.exists() and clientes.exists():
        print("Creando pedidos de prueba...")
        
        # Crear pedidos para el mes actual
        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)
        
        for i in range(10):  # Crear 10 pedidos
            vendedor = random.choice(vendedores)
            cliente = random.choice(clientes)
            
            # Fecha aleatoria en el mes actual
            dias_transcurridos = (hoy - inicio_mes).days
            if dias_transcurridos > 0:
                dia_random = random.randint(0, dias_transcurridos)
                fecha_pedido = inicio_mes + timedelta(days=dia_random)
            else:
                fecha_pedido = hoy
            
            # Monto aleatorio
            monto = Decimal(random.randint(50000, 500000))
            
            pedido = Pedido.objects.create(
                cliente=cliente,
                vendedor=vendedor,
                fecha=fecha_pedido,
                estado=random.choice([Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]),
                total=monto,
                iva_total=monto * Decimal('0.19')
            )
            
            print(f"✓ Pedido #{pedido.id} creado: ${monto} - {vendedor.user.username}")
        
        print("✅ Datos de prueba creados correctamente")
    else:
        print("❌ No hay vendedores o clientes para crear pedidos")

if __name__ == '__main__':
    if diagnostico_completo():
        respuesta = input("\n¿Deseas crear más datos de prueba? (s/n): ")
        if respuesta.lower() == 's':
            crear_datos_prueba_completos()
            print("\n✅ ¡Datos creados! Recarga la página del dashboard.")