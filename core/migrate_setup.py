"""
Vista para ejecutar migraciones desde la web
"""

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User, Group
from django.db import transaction
import sys
import io


@csrf_exempt
def migrate_and_setup(request):
    """Vista para ejecutar migraciones y configurar el sistema desde la web"""
    
    # Capturar la salida de los comandos
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        # Paso 1: Ejecutar migraciones
        print("🔄 Ejecutando migraciones...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✅ Migraciones completadas")
        
        # Paso 2: Crear grupos
        print("📋 Creando grupos...")
        groups_created = []
        for group_name in ['Gestor', 'JefeVentas', 'Vendedor']:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                groups_created.append(group_name)
                print(f"  ✅ Grupo '{group_name}' creado")
            else:
                print(f"  ℹ️ Grupo '{group_name}' ya existe")
        
        # Paso 3: Crear superusuario admin
        print("👑 Creando superusuario...")
        admin_created = False
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@rpgestor.com',
                password='admin123'
            )
            admin_created = True
            print("  ✅ Superusuario 'admin' creado")
        else:
            print("  ℹ️ Superusuario 'admin' ya existe")
        
        # Paso 4: Crear usuarios demo
        print("👥 Creando usuarios demo...")
        demo_users = [
            {
                'username': 'gestor1',
                'email': 'gestor1@demo.com',
                'password': 'demo123',
                'first_name': 'María',
                'last_name': 'Gestora',
                'group': 'Gestor',
                'is_superuser': True
            },
            {
                'username': 'jefe1',
                'email': 'jefe1@demo.com',
                'password': 'demo123',
                'first_name': 'Carlos',
                'last_name': 'Jefe',
                'group': 'JefeVentas',
                'is_superuser': False
            },
            {
                'username': 'vendedor1',
                'email': 'vendedor1@demo.com',
                'password': 'demo123',
                'first_name': 'Juan',
                'last_name': 'Vendedor',
                'group': 'Vendedor',
                'is_superuser': False
            }
        ]
        
        users_created = []
        for user_data in demo_users:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    is_staff=True,
                    is_active=True,
                    is_superuser=user_data['is_superuser']
                )
                
                # Asignar grupo
                try:
                    group = Group.objects.get(name=user_data['group'])
                    user.groups.add(group)
                    users_created.append(f"{user_data['username']} ({user_data['group']})")
                    print(f"  ✅ Usuario '{user_data['username']}' creado y asignado al grupo '{user_data['group']}'")
                except Group.DoesNotExist:
                    print(f"  ⚠️ Grupo '{user_data['group']}' no existe para usuario '{user_data['username']}'")
            else:
                print(f"  ℹ️ Usuario '{user_data['username']}' ya existe")
        
        # Paso 5: Crear registros de vendedor
        print("💼 Creando registros de vendedor...")
        vendedor_records_created = []
        try:
            from usuarios.models import Vendedor
            
            usernames = ['gestor1', 'jefe1', 'vendedor1']
            
            for username in usernames:
                try:
                    user = User.objects.get(username=username)
                    vendedor, created = Vendedor.objects.get_or_create(
                        user=user,
                        defaults={'presupuesto': 100000 if username == 'vendedor1' else 0}
                    )
                    
                    if created:
                        vendedor_records_created.append(username)
                        print(f"  ✅ Registro de vendedor creado para '{username}'")
                    else:
                        print(f"  ℹ️ Registro de vendedor ya existe para '{username}'")
                        
                except User.DoesNotExist:
                    print(f"  ⚠️ Usuario '{username}' no encontrado")
                    
        except ImportError:
            print("  ⚠️ Modelo Vendedor no disponible, omitiendo...")
        
        print("🎉 ¡Configuración completada exitosamente!")
        
        # Restaurar stdout
        sys.stdout = old_stdout
        output = captured_output.getvalue()
        
        # Generar respuesta HTML
        html_response = f"""
        <html>
        <head>
            <title>RPGestor - Migraciones y Configuración Completada</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; background: #f0f0f0; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; max-width: 900px; margin: 0 auto; }}
                .success {{ background: #dcfce7; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .info {{ background: #dbeafe; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .credentials {{ background: #fef3c7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .output {{ background: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0; font-family: monospace; white-space: pre-wrap; max-height: 300px; overflow-y: auto; }}
                .btn {{ background: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 5px; display: inline-block; }}
                .btn-success {{ background: #059669; }}
                .btn-warning {{ background: #d97706; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 style="color: #2563eb;">🎉 ¡Migraciones y Configuración Completadas!</h1>
                
                <div class="success">
                    <h3>✅ Proceso Exitoso</h3>
                    <p>Las migraciones se ejecutaron correctamente y el sistema ha sido configurado completamente.</p>
                </div>
                
                <div class="credentials">
                    <h3>🔑 Credenciales Disponibles:</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div>
                            <h4>🔐 Admin de Django:</h4>
                            <p><strong>Usuario:</strong> admin</p>
                            <p><strong>Contraseña:</strong> admin123</p>
                        </div>
                        <div>
                            <h4>👥 Usuarios de Demostración:</h4>
                            <p><strong>👔 Gestor:</strong> gestor1 / demo123</p>
                            <p><strong>👨‍💼 Jefe:</strong> jefe1 / demo123</p>
                            <p><strong>💼 Vendedor:</strong> vendedor1 / demo123</p>
                        </div>
                    </div>
                </div>
                
                <div class="info">
                    <h3>📋 Resumen de Configuración:</h3>
                    <ul>
                        <li><strong>Grupos creados:</strong> {', '.join(groups_created) if groups_created else 'Ya existían'}</li>
                        <li><strong>Admin:</strong> {'Creado' if admin_created else 'Ya existía'}</li>
                        <li><strong>Usuarios demo:</strong> {', '.join(users_created) if users_created else 'Ya existían'}</li>
                        <li><strong>Registros vendedor:</strong> {', '.join(vendedor_records_created) if vendedor_records_created else 'Ya existían'}</li>
                    </ul>
                </div>
                
                <div class="output">
                    <h4>📝 Log de Ejecución:</h4>
                    {output}
                </div>
                
                <div style="margin: 30px 0; text-align: center;">
                    <a href="/admin" class="btn">🔐 Ir al Admin de Django</a>
                    <a href="/" class="btn btn-success">🏠 Ir a la Aplicación</a>
                    <a href="/health/" class="btn btn-warning">🔍 Verificar Estado</a>
                </div>
                
                <div class="info">
                    <h3>🌐 URLs del Sistema:</h3>
                    <p><strong>Aplicación:</strong> <a href="https://rpgestor.onrender.com">https://rpgestor.onrender.com</a></p>
                    <p><strong>Admin:</strong> <a href="https://rpgestor.onrender.com/admin">https://rpgestor.onrender.com/admin</a></p>
                    <p><strong>Estado:</strong> <a href="https://rpgestor.onrender.com/health">https://rpgestor.onrender.com/health</a></p>
                </div>
                
                <p style="color: #6b7280; font-size: 14px; margin-top: 30px;">
                    ✅ El sistema está completamente configurado y listo para usar. 
                    Puede acceder con cualquiera de las credenciales mostradas arriba.
                </p>
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(html_response)
        
    except Exception as e:
        # Restaurar stdout en caso de error
        sys.stdout = old_stdout
        output = captured_output.getvalue()
        
        error_html = f"""
        <html>
        <head>
            <title>RPGestor - Error en Migraciones</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; background: #f0f0f0; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; max-width: 700px; margin: 0 auto; }}
                .error {{ background: #fecaca; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .output {{ background: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0; font-family: monospace; white-space: pre-wrap; max-height: 200px; overflow-y: auto; }}
                .btn {{ background: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 5px; }}
                .btn-danger {{ background: #dc2626; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 style="color: #dc2626;">❌ Error en Migraciones y Configuración</h1>
                
                <div class="error">
                    <h3>Error Detectado:</h3>
                    <p>{str(e)}</p>
                </div>
                
                <div class="output">
                    <h4>📝 Log de Ejecución:</h4>
                    {output}
                </div>
                
                <p>Por favor, contacte al administrador del sistema o intente con una de las opciones alternativas.</p>
                
                <div style="margin: 30px 0;">
                    <a href="/migrate-setup/" class="btn">🔄 Intentar de Nuevo</a>
                    <a href="/setup-admin/" class="btn">🛠️ Setup Básico</a>
                    <a href="/emergency-setup/" class="btn btn-danger">🚑 Setup de Emergencia</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(error_html)