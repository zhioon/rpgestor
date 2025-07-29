#!/usr/bin/env python
"""
Script para verificar que la configuración del servidor ASGI está correcta
"""
import os
import sys
import importlib.util

def check_django_settings():
    """Verificar que Django settings está configurado"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpgestor20.settings')
        import django
        django.setup()
        from django.conf import settings
        print("✅ Django settings configurado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en Django settings: {e}")
        return False

def check_channels():
    """Verificar que Channels está instalado y configurado"""
    try:
        import channels
        from django.conf import settings
        
        if 'channels' in settings.INSTALLED_APPS:
            print("✅ Channels instalado y configurado en INSTALLED_APPS")
        else:
            print("⚠️  Channels no está en INSTALLED_APPS")
            return False
            
        if hasattr(settings, 'ASGI_APPLICATION'):
            print(f"✅ ASGI_APPLICATION configurado: {settings.ASGI_APPLICATION}")
        else:
            print("❌ ASGI_APPLICATION no configurado")
            return False
            
        return True
    except ImportError:
        print("❌ Channels no está instalado. Instala con: pip install channels")
        return False
    except Exception as e:
        print(f"❌ Error verificando Channels: {e}")
        return False

def check_uvicorn():
    """Verificar que uvicorn está instalado"""
    try:
        import uvicorn
        print(f"✅ Uvicorn instalado: versión {uvicorn.__version__}")
        return True
    except ImportError:
        print("❌ Uvicorn no está instalado. Instala con: pip install uvicorn")
        return False

def check_redis():
    """Verificar configuración de Redis"""
    try:
        from django.conf import settings
        
        if hasattr(settings, 'CHANNEL_LAYERS'):
            channel_layers = settings.CHANNEL_LAYERS
            if 'default' in channel_layers:
                backend = channel_layers['default'].get('BACKEND')
                if 'redis' in backend.lower():
                    print("✅ Redis configurado como backend de Channel Layers")
                    
                    # Intentar conectar a Redis
                    try:
                        import redis
                        config = channel_layers['default'].get('CONFIG', {})
                        hosts = config.get('hosts', [('127.0.0.1', 6379)])
                        host, port = hosts[0]
                        
                        r = redis.Redis(host=host, port=port, decode_responses=True)
                        r.ping()
                        print(f"✅ Conexión a Redis exitosa ({host}:{port})")
                        return True
                    except Exception as e:
                        print(f"⚠️  Redis configurado pero no accesible: {e}")
                        print("💡 Asegúrate de que Redis esté ejecutándose")
                        return False
                else:
                    print("⚠️  Channel Layers no usa Redis")
                    return False
            else:
                print("❌ Channel Layers no tiene configuración 'default'")
                return False
        else:
            print("❌ CHANNEL_LAYERS no configurado")
            return False
    except Exception as e:
        print(f"❌ Error verificando Redis: {e}")
        return False

def check_asgi_file():
    """Verificar que el archivo ASGI existe y es válido"""
    try:
        from rpgestor20.asgi import application
        print("✅ Archivo ASGI importado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error importando ASGI: {e}")
        return False

def check_websocket_routing():
    """Verificar que el routing de WebSocket está configurado"""
    try:
        from notificaciones.routing import websocket_urlpatterns
        if websocket_urlpatterns:
            print(f"✅ WebSocket routing configurado ({len(websocket_urlpatterns)} rutas)")
            for pattern in websocket_urlpatterns:
                # Acceder correctamente al patrón regex
                try:
                    pattern_str = pattern.pattern.pattern if hasattr(pattern.pattern, 'pattern') else str(pattern.pattern)
                    print(f"   - {pattern_str}")
                except AttributeError:
                    # Fallback para diferentes versiones de Django
                    print(f"   - {pattern}")
        else:
            print("⚠️  No hay rutas WebSocket configuradas")
        return True
    except Exception as e:
        print(f"❌ Error verificando WebSocket routing: {e}")
        return False

def check_network_utils():
    """Verificar que las utilidades de red funcionen"""
    try:
        from network_utils import get_local_ip, get_network_info
        
        local_ip = get_local_ip()
        network_info = get_network_info()
        
        print(f"✅ IP local detectada: {local_ip}")
        print(f"✅ Rango de red: {network_info['network_range']}")
        
        if network_info['is_local_network']:
            print("✅ Red local detectada correctamente")
        else:
            print("⚠️  No se detectó red local (puede ser normal)")
        
        return True
    except Exception as e:
        print(f"❌ Error verificando utilidades de red: {e}")
        return False

def main():
    """Ejecutar todas las verificaciones"""
    print("🔍 Verificando configuración del servidor ASGI...")
    print("=" * 50)
    
    checks = [
        ("Django Settings", check_django_settings),
        ("Channels", check_channels),
        ("Uvicorn", check_uvicorn),
        ("Redis", check_redis),
        ("Archivo ASGI", check_asgi_file),
        ("WebSocket Routing", check_websocket_routing),
        ("Utilidades de Red", check_network_utils),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Verificando {name}...")
        result = check_func()
        results.append((name, result))
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VERIFICACIONES:")
    print("=" * 50)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 ¡Todas las verificaciones pasaron!")
        print("💡 Puedes ejecutar el servidor con:")
        print("   - python run_dev.py (desarrollo)")
        print("   - python run_asgi.py (producción)")
        print("   - python manage.py runasgi (comando Django)")
    else:
        print("⚠️  Algunas verificaciones fallaron.")
        print("💡 Revisa los errores arriba y corrígelos antes de ejecutar el servidor.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())