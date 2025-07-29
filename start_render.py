#!/usr/bin/env python
"""
Script de inicio simple para Render
"""
import os
import subprocess
import sys

def main():
    """Iniciar la aplicación Django con Gunicorn"""
    
    # Configurar variables de entorno
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpgestor20.settings_production')
    
    # Obtener puerto de Render
    port = os.environ.get('PORT', '10000')
    
    # Comando de Gunicorn
    cmd = [
        'gunicorn',
        'rpgestor20.wsgi:application',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '2',
        '--timeout', '120'
    ]
    
    print(f"🚀 Iniciando RPGestor en puerto {port}...")
    print(f"📝 Comando: {' '.join(cmd)}")
    
    # Ejecutar Gunicorn
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al iniciar Gunicorn: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()