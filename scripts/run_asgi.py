#!/usr/bin/env python
"""
Script para ejecutar el servidor ASGI con Channels en producción
Soluciona los problemas de importación temprana y configuración de Django
"""
import os
import sys
import argparse
from server_config import get_config
from network_utils import get_local_ip, print_network_info, get_network_interfaces_summary, find_available_port

def main():
    """Ejecutar el servidor ASGI con configuración correcta"""
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Servidor de producción Django ASGI')
    parser.add_argument('--network', action='store_true', 
                       help='Permitir conexiones desde la red local (detecta IP automáticamente)')
    parser.add_argument('--localhost', action='store_true', 
                       help='Solo permitir conexiones locales (127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000, 
                       help='Puerto del servidor (default: 8000)')
    parser.add_argument('--show-interfaces', action='store_true',
                       help='Mostrar todas las interfaces de red disponibles')
    
    args = parser.parse_args()
    
    # Configurar Django settings ANTES de cualquier importación
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpgestor20.settings')
    
    # Mostrar interfaces si se solicita
    if args.show_interfaces:
        get_network_interfaces_summary()
        return
    
    try:
        from uvicorn import run
        
        # Determinar host
        if args.localhost:
            host = "127.0.0.1"
        elif args.network:
            host = "0.0.0.0"  # Permite conexiones desde cualquier IP
        else:
            # Por defecto, preguntar al usuario
            local_ip = get_local_ip()
            print("🚀 CONFIGURACIÓN DEL SERVIDOR DE PRODUCCIÓN")
            print("=" * 50)
            print(f"🖥️  IP local detectada: {local_ip}")
            print()
            print("¿Cómo quieres ejecutar el servidor?")
            print("1. 🏠 Solo en esta computadora (localhost)")
            print("2. 🌐 Accesible desde la red local")
            print("3. 📋 Mostrar todas las interfaces de red")
            
            while True:
                choice = input("\nElige una opción (1/2/3): ").strip()
                if choice == "1":
                    host = "127.0.0.1"
                    break
                elif choice == "2":
                    host = "0.0.0.0"
                    break
                elif choice == "3":
                    get_network_interfaces_summary()
                    continue
                else:
                    print("❌ Opción inválida. Elige 1, 2 o 3.")
        
        # Verificar si el puerto está disponible
        port = args.port
        if not find_available_port(host if host != "0.0.0.0" else "127.0.0.1", port, 1):
            print(f"⚠️  Puerto {port} no disponible, buscando alternativo...")
            alternative_port = find_available_port(host if host != "0.0.0.0" else "127.0.0.1", port + 1)
            if alternative_port:
                port = alternative_port
                print(f"✅ Usando puerto alternativo: {port}")
            else:
                print("❌ No se encontró un puerto disponible")
                sys.exit(1)
        
        # Obtener configuración de producción y actualizarla
        config = get_config('production')
        config['host'] = host
        config['port'] = port
        
        print("\n🚀 Iniciando servidor ASGI de PRODUCCIÓN...")
        print_network_info(host, port)
        
        # Ejecutar servidor con configuración de producción
        run(**config)
        
    except ImportError as exc:
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
