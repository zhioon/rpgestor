"""
Utilidades para detectar y manejar configuración de red
"""
import socket
import subprocess
import platform
import sys

def get_local_ip():
    """
    Detecta automáticamente la IP local de la máquina
    Funciona en Windows, Linux y macOS
    """
    try:
        # Método 1: Conectar a un servidor externo (más confiable)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # No necesita conectarse realmente, solo obtiene la IP local
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            return local_ip
    except Exception:
        pass
    
    try:
        # Método 2: Obtener hostname y resolver IP
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        if local_ip != "127.0.0.1":
            return local_ip
    except Exception:
        pass
    
    try:
        # Método 3: Específico para Windows usando ipconfig
        if platform.system() == "Windows":
            result = subprocess.run(
                ["ipconfig"], 
                capture_output=True, 
                text=True, 
                encoding='utf-8'
            )
            lines = result.stdout.split('\n')
            for line in lines:
                if 'IPv4' in line and '192.168.' in line:
                    ip = line.split(':')[1].strip()
                    return ip
    except Exception:
        pass
    
    # Fallback: localhost
    return "127.0.0.1"

def get_network_info():
    """
    Obtiene información completa de la red
    """
    local_ip = get_local_ip()
    
    # Detectar el rango de red
    ip_parts = local_ip.split('.')
    network_range = "Red desconocida"
    is_local_network = False
    
    if len(ip_parts) == 4:
        if ip_parts[0] == '192' and ip_parts[1] == '168':
            network_range = f"192.168.{ip_parts[2]}.x"
            is_local_network = True
        elif ip_parts[0] == '10':
            network_range = f"10.x.x.x"
            is_local_network = True
        elif ip_parts[0] == '172' and 16 <= int(ip_parts[1]) <= 31:
            network_range = f"172.{ip_parts[1]}.x.x"
            is_local_network = True
        elif ip_parts[0] == '169' and ip_parts[1] == '254':
            network_range = "169.254.x.x (Link-local)"
            is_local_network = True
    
    return {
        'local_ip': local_ip,
        'network_range': network_range,
        'is_local_network': is_local_network
    }

def get_all_network_interfaces():
    """
    Obtiene todas las interfaces de red disponibles
    """
    interfaces = []
    
    try:
        if platform.system() == "Windows":
            # Método más simple y robusto para Windows
            local_ip = get_local_ip()
            
            # Agregar la IP principal
            interfaces.append({
                'name': 'Adaptador principal',
                'ip': local_ip
            })
            
            # Intentar obtener interfaces adicionales de forma segura
            try:
                # Usar encoding más seguro para Windows
                result = subprocess.run(
                    ["ipconfig"], 
                    capture_output=True, 
                    text=False  # No usar text=True para evitar problemas de codificación
                )
                
                # Decodificar manualmente con manejo de errores
                output = result.stdout.decode('cp1252', errors='replace')
                lines = output.split('\n')
                current_adapter = None
                
                for line in lines:
                    line = line.strip()
                    if 'adaptador' in line.lower() or 'adapter' in line.lower():
                        current_adapter = line
                    elif 'IPv4' in line and ':' in line:
                        try:
                            ip = line.split(':')[1].strip()
                            if ip and ip != "127.0.0.1" and ip != local_ip:
                                interfaces.append({
                                    'name': current_adapter or 'Adaptador adicional',
                                    'ip': ip
                                })
                        except:
                            pass
            except Exception:
                # Si falla, al menos tenemos la IP principal
                pass
        else:
            # Para Linux/macOS
            try:
                result = subprocess.run(
                    ["ifconfig"], 
                    capture_output=True, 
                    text=True
                )
                # Parsing básico para ifconfig
                lines = result.stdout.split('\n')
                current_interface = None
                
                for line in lines:
                    if line and not line.startswith(' ') and not line.startswith('\t'):
                        current_interface = line.split(':')[0]
                    elif 'inet ' in line and '127.0.0.1' not in line:
                        ip = line.split('inet ')[1].split(' ')[0]
                        if current_interface:
                            interfaces.append({
                                'name': current_interface,
                                'ip': ip
                            })
            except:
                # Si falla, usar el método simple
                local_ip = get_local_ip()
                interfaces.append({
                    'name': 'Interfaz principal',
                    'ip': local_ip
                })
    except Exception as e:
        # Fallback: al menos agregar la IP principal
        try:
            local_ip = get_local_ip()
            interfaces.append({
                'name': 'IP detectada',
                'ip': local_ip
            })
        except:
            pass
    
    # Si no se encontró ninguna interfaz, agregar la IP principal
    if not interfaces:
        try:
            local_ip = get_local_ip()
            interfaces.append({
                'name': 'IP detectada',
                'ip': local_ip
            })
        except:
            pass
    
    return interfaces

def is_port_available(host, port):
    """
    Verifica si un puerto está disponible
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            return result != 0
    except Exception:
        return False

def find_available_port(host, start_port=8000, max_attempts=10):
    """
    Encuentra un puerto disponible comenzando desde start_port
    """
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(host, port):
            return port
    return None

def print_network_info(host, port):
    """
    Imprime información de red útil para el usuario
    """
    local_ip = get_local_ip()
    
    print("🌐 INFORMACIÓN DE RED:")
    print("=" * 50)
    print(f"🖥️  IP Local detectada: {local_ip}")
    print(f"🚀 Servidor ejecutándose en: {host}:{port}")
    print()
    
    if host == "0.0.0.0":
        print("📱 ACCESO DESDE OTROS DISPOSITIVOS:")
        print(f"   • Desde tu computadora: http://localhost:{port}/")
        print(f"   • Desde otros dispositivos: http://{local_ip}:{port}/")
        print()
        print("📡 WEBSOCKETS DISPONIBLES:")
        print(f"   • Notificaciones: ws://{local_ip}:{port}/ws/notificaciones/")
        print(f"   • Mensajes: ws://{local_ip}:{port}/ws/mensajes/")
        print()
        print("📋 PARA CONECTAR DESDE MÓVIL/TABLET:")
        print(f"   1. Asegúrate de estar en la misma red WiFi")
        print(f"   2. Abre el navegador y ve a: http://{local_ip}:{port}/")
        print(f"   3. Si no funciona, verifica el firewall de Windows")
    else:
        print("📋 ACCESO:")
        print(f"   • Solo desde esta computadora: http://{host}:{port}/")
        print("   • Para acceso desde red local, usa el modo --network")
    
    print()
    print("🔥 FIREWALL DE WINDOWS:")
    print("   Si otros dispositivos no pueden conectar:")
    print("   1. Ve a 'Configuración de Windows Defender Firewall'")
    print(f"   2. Permite la aplicación Python en puerto {port}")
    print("   3. O temporalmente desactiva el firewall para testing")
    print("=" * 50)

def get_network_interfaces_summary():
    """
    Obtiene un resumen de las interfaces de red
    """
    interfaces = get_all_network_interfaces()
    local_ip = get_local_ip()
    
    print("🔍 INTERFACES DE RED DETECTADAS:")
    print("-" * 30)
    
    if interfaces:
        for i, interface in enumerate(interfaces, 1):
            status = "🟢 PRINCIPAL" if interface['ip'] == local_ip else "🔵 DISPONIBLE"
            print(f"{i}. {interface['name']}")
            print(f"   IP: {interface['ip']} {status}")
    else:
        print("⚠️  No se detectaron interfaces adicionales")
        print(f"🔵 IP por defecto: {local_ip}")
    
    print("-" * 30)
    return interfaces