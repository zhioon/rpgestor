#!/usr/bin/env python
"""
Script rápido para ejecutar el servidor en modo red local
Detecta automáticamente la IP y permite conexiones desde otros dispositivos
"""
import os
import sys
from server_config import get_config
from network_utils import get_local_ip, print_network_info, find_available_port

def main():
    """Ejecutar servidor accesible desde la red local"""
    # Configurar Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpgestor20.settings')
    
    try:
        from uvicorn import run
        
        # Detectar IP local
        local_ip = get_local_ip()
        host = "0.0.0.0"  # Permite conexiones desde cualquier IP
        port = 8000
        
        # Verificar puerto disponible
        if not find_available_port("127.0.0.1", port, 1):
            alternative_port = find_available_port("127.0.0.1", port + 1)
            if alternative_port:
                port = alternative_port
                print(f"✅ Usando puerto alternativo: {port}")
            else:
                print("❌ No se encontró un puerto disponible")
                sys.exit(1)
        
        # Obtener configuración de desarrollo y actualizarla
        config = get_config('development')
        config['host'] = host
        config['port'] = port
        
        print("🌐 SERVIDOR DE RED LOCAL")
        print("=" * 50)
        print(f"🖥️  IP detectada: {local_ip}")
        print("🚀 Iniciando servidor accesible desde la red local...")
        print_network_info(host, port)
        
        # Ejecutar servidor
        run(**config)
        
    except ImportError:
        print("❌ Error: No se pudo importar uvicorn.")
        print("💡 Instala uvicorn con: pip install uvicorn")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido por el usuario")
        sys.exit(0)
    except Exception as exc:
        print(f"❌ Error al iniciar el servidor: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main()