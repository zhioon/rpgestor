"""
Vista para configurar superusuarios desde la web
"""

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.db import transaction


@csrf_exempt
def setup_admin(request):
    """Vista para crear superusuario desde la web"""
    try:
        with transaction.atomic():
            # Crear grupos
            groups_created = []
            for group_name in ['Gestor', 'JefeVentas', 'Vendedor']:
                group, created = Group.objects.get_or_create(name=group_name)
                if created:
                    groups_created.append(group_name)
            
            # Crear o actualizar superusuario admin
            admin_user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@rpgestor.com',
                    'is_superuser': True,
                    'is_staff': True,
                }
            )
            
            # Establecer contraseña
            admin_user.set_password('admin123')
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()
            
            # Crear usuario gestor también
            gestor_user, created2 = User.objects.get_or_create(
                username='gestor1',
                defaults={
                    'email': 'gestor1@rpgestor.com',
                    'is_superuser': True,
                    'is_staff': True,
                    'first_name': 'María',
                    'last_name': 'Gestora'
                }
            )
            
            gestor_user.set_password('demo123')
            gestor_user.is_superuser = True
            gestor_user.is_staff = True
            gestor_user.save()
            
            # Asignar grupo al gestor
            try:
                gestor_group = Group.objects.get(name='Gestor')
                gestor_user.groups.add(gestor_group)
            except Group.DoesNotExist:
                pass
            
            # Crear usuario jefe1
            jefe_user, created3 = User.objects.get_or_create(
                username='jefe1',
                defaults={
                    'email': 'jefe1@demo.com',
                    'is_staff': True,
                    'first_name': 'Carlos',
                    'last_name': 'Jefe'
                }
            )
            
            jefe_user.set_password('demo123')
            jefe_user.is_staff = True
            jefe_user.save()
            
            # Asignar grupo al jefe
            try:
                jefe_group = Group.objects.get(name='JefeVentas')
                jefe_user.groups.add(jefe_group)
            except Group.DoesNotExist:
                pass
            
            # Crear usuario vendedor1
            vendedor_user, created4 = User.objects.get_or_create(
                username='vendedor1',
                defaults={
                    'email': 'vendedor1@demo.com',
                    'is_staff': True,
                    'first_name': 'Juan',
                    'last_name': 'Vendedor'
                }
            )
            
            vendedor_user.set_password('demo123')
            vendedor_user.is_staff = True
            vendedor_user.save()
            
            # Asignar grupo al vendedor
            try:
                vendedor_group = Group.objects.get(name='Vendedor')
                vendedor_user.groups.add(vendedor_group)
            except Group.DoesNotExist:
                pass
            
            # Crear registros de vendedor
            vendedor_records_created = []
            try:
                from usuarios.models import Vendedor
                for username in ['gestor1', 'jefe1', 'vendedor1']:
                    try:
                        user = User.objects.get(username=username)
                        vendedor_obj, created = Vendedor.objects.get_or_create(
                            user=user,
                            defaults={'presupuesto': 100000 if username == 'vendedor1' else 0}
                        )
                        if created:
                            vendedor_records_created.append(username)
                    except User.DoesNotExist:
                        pass
            except ImportError:
                pass
        
        return HttpResponse(f"""
        <html>
        <head><title>RPGestor - Admin Setup</title></head>
        <body style="font-family: Arial; padding: 20px; background: #f0f0f0;">
            <div style="background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto;">
                <h1 style="color: #2563eb;">🎉 ¡Superusuarios Creados Exitosamente!</h1>
                
                <div style="background: #dcfce7; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3>✅ Credenciales de Admin:</h3>
                    <p><strong>Usuario:</strong> admin</p>
                    <p><strong>Contraseña:</strong> admin123</p>
                </div>
                
                <div style="background: #dbeafe; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3>✅ Credenciales de Demostración:</h3>
                    <p><strong>👔 Gestor:</strong> gestor1 / demo123</p>
                    <p><strong>👨‍💼 Jefe:</strong> jefe1 / demo123</p>
                    <p><strong>💼 Vendedor:</strong> vendedor1 / demo123</p>
                </div>
                
                <div style="background: #fef3c7; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3>📋 Elementos Creados:</h3>
                    <p><strong>Grupos:</strong> {', '.join(groups_created) if groups_created else 'Ya existían'}</p>
                    <p><strong>Registros Vendedor:</strong> {', '.join(vendedor_records_created) if vendedor_records_created else 'Ya existían'}</p>
                </div>
                
                <div style="margin: 30px 0;">
                    <a href="/admin" style="background: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-right: 10px;">🔐 Ir al Admin</a>
                    <a href="/" style="background: #059669; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">🏠 Ir a la Aplicación</a>
                </div>
                
                <p style="color: #6b7280; font-size: 14px;">Nota: Estas credenciales son para demostración. En producción real, usa contraseñas más seguras.</p>
            </div>
        </body>
        </html>
        """)
        
    except Exception as e:
        return HttpResponse(f"""
        <html>
        <head><title>Error - Admin Setup</title></head>
        <body style="font-family: Arial; padding: 20px; background: #f0f0f0;">
            <div style="background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto;">
                <h1 style="color: #dc2626;">❌ Error al Crear Superusuario</h1>
                <p>Error: {str(e)}</p>
                <a href="/setup-admin" style="background: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">🔄 Intentar de Nuevo</a>
                <a href="/emergency-setup" style="background: #059669; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-left: 10px;">🚑 Setup de Emergencia</a>
            </div>
        </body>
        </html>
        """)