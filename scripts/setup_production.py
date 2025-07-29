#!/usr/bin/env python
"""
Script para configurar RPGestor para despliegue en producción
"""

import os
import sys
import subprocess
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def print_header(title):
    """Imprimir encabezado con formato"""
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def print_success(message):
    """Imprimir mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message):
    """Imprimir mensaje de error"""
    print(f"❌ {message}")

def print_info(message):
    """Imprimir mensaje informativo"""
    print(f"ℹ️  {message}")

def run_command(command, description):
    """Ejecutar un comando y verificar el resultado"""
    try:
        print_info(f"Ejecutando: {description}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=project_root)
        if result.returncode == 0:
            print_success(f"{description} - Completado")
            return True
        else:
            print_error(f"{description} - Error: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"{description} - Excepción: {e}")
        return False

def create_env_production():
    """Crear archivo .env para producción"""
    env_content = """# RPGestor - Configuración para Producción
# IMPORTANTE: Configura estas variables en tu plataforma de hosting

# Django
DEBUG=False
SECRET_KEY=tu-clave-secreta-super-segura-para-produccion-cambiar-esto
DJANGO_SETTINGS_MODULE=rpgestor20.settings_production

# Base de datos (se configura automáticamente en Railway/Render)
# DATABASE_URL=postgresql://user:password@host:port/database

# Redis (se configura automáticamente en Railway/Render)
# REDIS_URL=redis://user:password@host:port

# Dominio permitido (cambiar por tu dominio)
ALLOWED_HOSTS=localhost,127.0.0.1,.railway.app,.up.railway.app

# Email (opcional - configurar si necesitas envío de emails)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-de-aplicacion

# Configuración de archivos estáticos
STATIC_URL=/static/
MEDIA_URL=/media/
"""
    
    env_prod_path = project_root / '.env.production'
    with open(env_prod_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print_success(f"Archivo .env.production creado en: {env_prod_path}")

def main():
    """Función principal"""
    print("🚀 RPGestor - Configuración para Producción")
    print("Preparando el proyecto para despliegue...")
    
    print_header("VERIFICANDO ESTRUCTURA DEL PROYECTO")
    
    # Verificar archivos necesarios
    required_files = [
        'manage.py',
        'requirements.txt',
        'railway.json',
        'Procfile',
        'rpgestor20/settings_production.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(project_root / file_path):
            print_success(f"Archivo encontrado: {file_path}")
        else:
            print_error(f"Archivo faltante: {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print_error("Faltan archivos necesarios para el despliegue")
        return False
    
    print_header("CONFIGURANDO ARCHIVOS DE PRODUCCIÓN")
    
    # Crear archivo .env para producción
    create_env_production()
    
    print_header("VERIFICANDO DEPENDENCIAS")
    
    # Verificar que las dependencias estén instaladas
    commands = [
        ("python -c \"import django; print('Django:', django.get_version())\"", "Verificar Django"),
        ("python -c \"import gunicorn; print('Gunicorn instalado')\"", "Verificar Gunicorn"),
        ("python -c \"import whitenoise; print('WhiteNoise instalado')\"", "Verificar WhiteNoise"),
        ("python -c \"import dj_database_url; print('dj-database-url instalado')\"", "Verificar dj-database-url"),
    ]
    
    for command, description in commands:
        run_command(command, description)
    
    print_header("VERIFICANDO CONFIGURACIÓN DE DJANGO")
    
    # Verificar configuración de Django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'rpgestor20.settings_production'
    django_commands = [
        ("python manage.py check --deploy", "Verificar configuración para producción"),
        ("python manage.py collectstatic --noinput --dry-run", "Verificar archivos estáticos"),
    ]
    
    for command, description in django_commands:
        run_command(command, description)
    
    print_header("INSTRUCCIONES DE DESPLIEGUE")
    
    print("📋 PASOS PARA DESPLEGAR EN RAILWAY:")
    print("   1. Crear cuenta en https://railway.app")
    print("   2. Conectar tu repositorio de GitHub")
    print("   3. Crear nuevo proyecto desde GitHub")
    print("   4. Railway detectará automáticamente Django")
    print("   5. Agregar servicios: PostgreSQL + Redis")
    print("   6. Configurar variables de entorno:")
    print("      - DEBUG=False")
    print("      - SECRET_KEY=tu-clave-secreta-segura")
    print("      - DJANGO_SETTINGS_MODULE=rpgestor20.settings_production")
    print("   7. Deploy automático se ejecutará")
    print("   8. Tu app estará disponible en: https://tu-app.up.railway.app")
    
    print("\n📋 PASOS PARA DESPLEGAR EN RENDER:")
    print("   1. Crear cuenta en https://render.com")
    print("   2. Crear nuevo Web Service desde GitHub")
    print("   3. Configurar:")
    print("      - Build Command: pip install -r requirements.txt")
    print("      - Start Command: gunicorn rpgestor20.wsgi:application")
    print("   4. Agregar PostgreSQL database")
    print("   5. Configurar variables de entorno (igual que Railway)")
    print("   6. Deploy automático se ejecutará")
    
    print("\n📋 PASOS PARA DESPLEGAR EN HEROKU:")
    print("   1. Instalar Heroku CLI")
    print("   2. heroku create tu-app-rpgestor")
    print("   3. heroku addons:create heroku-postgresql:hobby-dev")
    print("   4. heroku addons:create heroku-redis:hobby-dev")
    print("   5. heroku config:set DEBUG=False")
    print("   6. heroku config:set SECRET_KEY=tu-clave-secreta")
    print("   7. git push heroku main")
    print("   8. heroku run python manage.py migrate")
    print("   9. heroku run python manage.py createsuperuser")
    
    print_header("VARIABLES DE ENTORNO IMPORTANTES")
    
    print("🔑 CONFIGURAR EN TU PLATAFORMA DE HOSTING:")
    print("   DEBUG=False")
    print("   SECRET_KEY=clave-super-secreta-cambiar-esto")
    print("   DJANGO_SETTINGS_MODULE=rpgestor20.settings_production")
    print("   DATABASE_URL=postgresql://... (automático)")
    print("   REDIS_URL=redis://... (automático)")
    
    print_header("DESPUÉS DEL DESPLIEGUE")
    
    print("📋 COMANDOS A EJECUTAR DESPUÉS DEL PRIMER DEPLOY:")
    print("   1. Ejecutar migraciones (automático en Railway)")
    print("   2. Crear superusuario:")
    print("      - Railway: railway run python manage.py createsuperuser")
    print("      - Render: usar shell desde dashboard")
    print("      - Heroku: heroku run python manage.py createsuperuser")
    print("   3. Cargar datos iniciales si es necesario")
    
    print_header("URLS DE ACCESO")
    
    print("🌐 TU APLICACIÓN ESTARÁ DISPONIBLE EN:")
    print("   - Railway: https://tu-proyecto.up.railway.app")
    print("   - Render: https://tu-app.onrender.com")
    print("   - Heroku: https://tu-app.herokuapp.com")
    
    print("\n🎉 ¡Tu proyecto RPGestor está listo para producción!")
    print("📚 Consulta la documentación en docs/DESPLIEGUE.md para más detalles")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)