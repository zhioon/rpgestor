"""
Configuración centralizada para diferentes tipos de servidor
"""
import os
from network_utils import get_local_ip, print_network_info

# Configuración base
BASE_CONFIG = {
    'host': '127.0.0.1',
    'port': 8000,
    'app': 'rpgestor20.asgi:application',
    'ws': 'auto',  # <-- AÑADIDO: Detección automática de WebSockets
    'log_level': 'info',
    'access_log': True,
}

# Configuración para producción
PRODUCTION_CONFIG = {
    **BASE_CONFIG,
    'reload': False,
    'workers': 1,  # Para ASGI, generalmente 1 worker es suficiente
    'log_level': 'warning',
}

# Configuración para desarrollo
DEVELOPMENT_CONFIG = {
    **BASE_CONFIG,
    'reload': True,
    'reload_dirs': ['./'],
    'reload_excludes': ['venv', '__pycache__', '*.pyc', '.git', '*.sqlite3'],
    'log_level': 'debug',
}

# Configuración para desarrollo en red local
NETWORK_DEVELOPMENT_CONFIG = {
    **DEVELOPMENT_CONFIG,
    'host': '0.0.0.0',  # Acepta conexiones de cualquier IP
}

# Configuración para testing
TESTING_CONFIG = {
    **BASE_CONFIG,
    'reload': False,
    'log_level': 'error',
    'access_log': False,
}

def get_config(environment='development', network_access=False):
    """
    Obtiene la configuración para el entorno especificado
    
    Args:
        environment (str): 'development', 'production', o 'testing'
        network_access (bool): Si True, permite acceso desde la red local
    
    Returns:
        dict: Configuración del servidor
    """
    configs = {
        'development': NETWORK_DEVELOPMENT_CONFIG if network_access else DEVELOPMENT_CONFIG,
        'production': PRODUCTION_CONFIG,
        'testing': TESTING_CONFIG,
    }
    
    config = configs.get(environment, DEVELOPMENT_CONFIG)
    
    # Si se solicita acceso de red, cambiar host a 0.0.0.0
    if network_access and environment != 'testing':
        config = {**config, 'host': '0.0.0.0'}
    
    return config

def print_server_info(config, show_network_info=True):
    """Imprime información del servidor"""
    host = config['host']
    port = config['port']
    
    print("🚀 Iniciando servidor ASGI con Channels...")
    
    if config.get('reload'):
        print("🔄 Reload automático: ACTIVADO")
    else:
        print("🔄 Reload automático: DESACTIVADO")
    
    print("⚠️  Para detener el servidor: Ctrl+C")
    print()
    
    if show_network_info:
        print_network_info(host, port)
    else:
        print("📡 WebSockets disponibles en:")
        print(f"   - ws://{host}:{port}/ws/notificaciones/")
        print(f"   - ws://{host}:{port}/ws/mensajes/")
        print(f"🌐 HTTP disponible en: http://{host}:{port}/")
        print("-" * 50)