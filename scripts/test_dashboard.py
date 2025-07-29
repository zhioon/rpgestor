#!/usr/bin/env python
"""
Script para probar el dashboard de jefe de ventas
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
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

def verificar_datos():
    """Verificar que existan datos básicos para el dashboard"""
    
    print("=== VERIFICACIÓN DE DATOS PARA DASHBOARD ===")
    
    # Verificar usuarios y grupos
    jefe_ventas_group, created = Group.objects.get_or_create(name='JefeVentas')
    vendedor_group, created = Group.objects.get_or_create(name='Vendedor')
    
    print(f"✓ Grupos creados: JefeVentas, Vendedor")
    
    # Verificar vendedores
    vendedores = Vendedor.objects.all()
    print(f"✓ Vendedores en sistema: {vendedores.count()}")
    
    vendedores_sin_usuario = Vendedor.objects.filter(user__isnull=True)
    if vendedores_sin_usuario.exists():
        print(f"⚠️  Vendedores sin usuario asociado: {vendedores_sin_usuario.count()}")
    
    # Verificar pedidos
    pedidos = Pedido.objects.all()
    print(f"✓ Pedidos en sistema: {pedidos.count()}")
    
    pedidos_con_vendedor = Pedido.objects.filter(vendedor__isnull=False)
    print(f"✓ Pedidos con vendedor: {pedidos_con_vendedor.count()}")
    
    # Verificar pedidos del mes actual
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    pedidos_mes = Pedido.objects.filter(
        fecha__gte=inicio_mes,
        estado__in=[Pedido.Estado.ENVIADO, Pedido.Estado.FINALIZADO]
    )
    print(f"✓ Pedidos finalizados este mes: {pedidos_mes.count()}")
    
    # Verificar clientes
    clientes = Cliente.objects.all()
    print(f"✓ Clientes en sistema: {clientes.count()}")
    
    # Verificar productos
    productos = Producto.objects.all()
    print(f"✓ Productos en sistema: {productos.count()}")
    
    print("\n=== RESUMEN ===")
    if vendedores.count() > 0 and pedidos.count() > 0:
        print("✅ El sistema tiene datos suficientes para mostrar el dashboard")
    else:
        print("⚠️  El sistema necesita más datos para mostrar información útil")
        
    return True

def crear_datos_prueba():
    """Crear algunos datos de prueba si no existen"""
    
    print("\n=== CREANDO DATOS DE PRUEBA ===")
    
    # Crear usuario jefe de ventas si no existe
    jefe_user, created = User.objects.get_or_create(
        username='jefe_ventas',
        defaults={
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'email': 'jefe@empresa.com',
            'is_staff': True
        }
    )
    
    if created:
        jefe_user.set_password('123456')
        jefe_user.save()
        print("✓ Usuario jefe de ventas creado")
    
    # Agregar al grupo
    jefe_ventas_group = Group.objects.get(name='JefeVentas')
    jefe_user.groups.add(jefe_ventas_group)
    
    # Crear algunos vendedores de prueba si no existen
    vendedores_data = [
        {'username': 'vendedor1', 'first_name': 'María', 'last_name': 'García', 'presupuesto': 100000},
        {'username': 'vendedor2', 'first_name': 'Carlos', 'last_name': 'López', 'presupuesto': 80000},
        {'username': 'vendedor3', 'first_name': 'Ana', 'last_name': 'Martínez', 'presupuesto': 90000},
    ]
    
    vendedor_group = Group.objects.get(name='Vendedor')
    
    for data in vendedores_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': f"{data['username']}@empresa.com"
            }
        )
        
        if created:
            user.set_password('123456')
            user.save()
            user.groups.add(vendedor_group)
            print(f"✓ Usuario {data['username']} creado")
        
        # Crear vendedor
        vendedor, created = Vendedor.objects.get_or_create(
            user=user,
            defaults={'presupuesto': Decimal(str(data['presupuesto']))}
        )
        
        if created:
            print(f"✓ Vendedor {data['first_name']} {data['last_name']} creado")
    
    print("✅ Datos de prueba creados correctamente")

if __name__ == '__main__':
    verificar_datos()
    
    respuesta = input("\n¿Deseas crear datos de prueba? (s/n): ")
    if respuesta.lower() == 's':
        crear_datos_prueba()
        print("\n✅ ¡Listo! Ahora puedes probar el dashboard de jefe de ventas")
        print("Usuario: jefe_ventas")
        print("Contraseña: 123456")
        print("URL: /usuarios/dashboard/jefeventas/completo/")