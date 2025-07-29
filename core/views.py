from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.db import transaction
from .models import TestModel
from .utils import export_queryset_to_csv

def export_tests(request):
    """
    Exporta todas las instancias de TestModel a un CSV descargable.
    """
    qs = TestModel.objects.all()
    return export_queryset_to_csv(
        queryset=qs,
        fields=['id', 'name', 'created_at', 'updated_at'],
        filename='testmodels.csv'
    )


def emergency_setup(request):
    """
    Vista de emergencia para configurar el sistema cuando fallan otros métodos
    """
    try:
        with transaction.atomic():
            # Crear grupos
            groups_created = []
            for group_name in ['Gestor', 'JefeVentas', 'Vendedor']:
                group, created = Group.objects.get_or_create(name=group_name)
                if created:
                    groups_created.append(group_name)
            
            # Crear superusuario admin
            admin_created = False
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@rpgestor.com',
                    password='admin123'
                )
                admin_created = True
            
            # Crear usuario gestor1
            gestor_created = False
            if not User.objects.filter(username='gestor1').exists():
                gestor_user = User.objects.create_superuser(
                    username='gestor1',
                    email='gestor1@demo.com',
                    password='demo123',
                    first_name='María',
                    last_name='Gestora'
                )
                try:
                    gestor_group = Group.objects.get(name='Gestor')
                    gestor_user.groups.add(gestor_group)
                except Group.DoesNotExist:
                    pass
                gestor_created = True
            
            # Crear usuario jefe1
            jefe_created = False
            if not User.objects.filter(username='jefe1').exists():
                jefe_user = User.objects.create_user(
                    username='jefe1',
                    email='jefe1@demo.com',
                    password='demo123',
                    first_name='Carlos',
                    last_name='Jefe',
                    is_staff=True
                )
                try:
                    jefe_group = Group.objects.get(name='JefeVentas')
                    jefe_user.groups.add(jefe_group)
                except Group.DoesNotExist:
                    pass
                jefe_created = True
            
            # Crear usuario vendedor1
            vendedor_created = False
            if not User.objects.filter(username='vendedor1').exists():
                vendedor_user = User.objects.create_user(
                    username='vendedor1',
                    email='vendedor1@demo.com',
                    password='demo123',
                    first_name='Juan',
                    last_name='Vendedor',
                    is_staff=True
                )
                try:
                    vendedor_group = Group.objects.get(name='Vendedor')
                    vendedor_user.groups.add(vendedor_group)
                except Group.DoesNotExist:
                    pass
                vendedor_created = True
            
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
        
        # Generar respuesta HTML
        html_response = f"""
        <html>
        <head>
            <title>RPGestor - Configuración de Emergencia</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; background: #f0f0f0; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; max-width: 800px; margin: 0 auto; }}
                .success {{ background: #dcfce7; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .info {{ background: #dbeafe; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .credentials {{ background: #fef3c7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .btn {{ background: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 5px; display: inline-block; }}
                .btn-success {{ background: #059669; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 style="color: #2563eb;">🚑 Configuración de Emergencia Completada</h1>
                
                <div class="success">
                    <h3>✅ Configuración Exitosa</h3>
                    <p>El sistema ha sido configurado correctamente usando el método de emergencia.</p>
                </div>
                
                <div class="info">
                    <h3>📋 Elementos Creados:</h3>
                    <ul>
                        <li><strong>Grupos:</strong> {', '.join(groups_created) if groups_created else 'Ya existían'}</li>
                        <li><strong>Admin:</strong> {'Creado' if admin_created else 'Ya existía'}</li>
                        <li><strong>Gestor1:</strong> {'Creado' if gestor_created else 'Ya existía'}</li>
                        <li><strong>Jefe1:</strong> {'Creado' if jefe_created else 'Ya existía'}</li>
                        <li><strong>Vendedor1:</strong> {'Creado' if vendedor_created else 'Ya existía'}</li>
                        <li><strong>Registros Vendedor:</strong> {', '.join(vendedor_records_created) if vendedor_records_created else 'Ya existían'}</li>
                    </ul>
                </div>
                
                <div class="credentials">
                    <h3>🔑 Credenciales Disponibles:</h3>
                    <p><strong>👔 Admin:</strong> admin / admin123</p>
                    <p><strong>👔 Gestor:</strong> gestor1 / demo123</p>
                    <p><strong>👨‍💼 Jefe:</strong> jefe1 / demo123</p>
                    <p><strong>💼 Vendedor:</strong> vendedor1 / demo123</p>
                </div>
                
                <div style="margin: 30px 0;">
                    <a href="/admin" class="btn">🔐 Ir al Admin</a>
                    <a href="/" class="btn btn-success">🏠 Ir a la Aplicación</a>
                    <a href="/setup-admin/" class="btn">🛠️ Setup Alternativo</a>
                </div>
                
                <div class="info">
                    <h3>🌐 URLs del Sistema:</h3>
                    <p><strong>Aplicación:</strong> https://rpgestor.onrender.com</p>
                    <p><strong>Admin:</strong> https://rpgestor.onrender.com/admin</p>
                    <p><strong>Setup:</strong> https://rpgestor.onrender.com/setup-admin</p>
                </div>
                
                <p style="color: #6b7280; font-size: 14px; margin-top: 30px;">
                    Esta configuración de emergencia se ejecutó exitosamente. 
                    El sistema está listo para usar con las credenciales mostradas arriba.
                </p>
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(html_response)
        
    except Exception as e:
        error_html = f"""
        <html>
        <head>
            <title>RPGestor - Error de Configuración</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; background: #f0f0f0; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto; }}
                .error {{ background: #fecaca; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .btn {{ background: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 style="color: #dc2626;">❌ Error en Configuración de Emergencia</h1>
                
                <div class="error">
                    <h3>Error Detectado:</h3>
                    <p>{str(e)}</p>
                </div>
                
                <p>Por favor, contacte al administrador del sistema o intente nuevamente.</p>
                
                <div style="margin: 30px 0;">
                    <a href="/emergency-setup/" class="btn">🔄 Intentar de Nuevo</a>
                    <a href="/setup-admin/" class="btn">🛠️ Setup Alternativo</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(error_html)


# Create your views here.
