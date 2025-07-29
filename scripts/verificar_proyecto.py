#!/usr/bin/env python
"""
Script para verificar que el proyecto RPGestor esté correctamente organizado y funcional.
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def print_header(title):
    """Imprimir encabezado con formato"""
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def print_success(message):
    """Imprimir mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message):
    """Imprimir mensaje de error"""
    print(f"❌ {message}")

def print_warning(message):
    """Imprimir mensaje de advertencia"""
    print(f"⚠️  {message}")

def check_file_exists(file_path, description):
    """Verificar si un archivo existe"""
    if os.path.exists(file_path):
        print_success(f"{description}: {file_path}")
        return True
    else:
        print_error(f"{description} no encontrado: {file_path}")
        return False

def check_directory_exists(dir_path, description):
    """Verificar si un directorio existe"""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        print_success(f"{description}: {dir_path}")
        return True
    else:
        print_error(f"{description} no encontrado: {dir_path}")
        return False

def check_python_module(module_name):
    """Verificar si un módulo de Python puede ser importado"""
    try:
        importlib.import_module(module_name)
        print_success(f"Módulo Python: {module_name}")
        return True
    except ImportError as e:
        print_error(f"Error importando {module_name}: {e}")
        return False

def run_command(command, description):
    """Ejecutar un comando y verificar el resultado"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=project_root)
        if result.returncode == 0:
            print_success(f"{description}")
            return True
        else:
            print_error(f"{description} - Error: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"{description} - Excepción: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🚀 RPGestor - Verificación de Proyecto")
    print("Verificando la organización y funcionalidad del proyecto...")
    
    total_checks = 0
    passed_checks = 0
    
    # 1. Verificar estructura de archivos principales
    print_header("ESTRUCTURA DE ARCHIVOS PRINCIPALES")
    
    main_files = [
        ("manage.py", "Script principal de Django"),
        ("requirements.txt", "Dependencias del proyecto"),
        ("README.md", "Documentación principal"),
        ("CHANGELOG.md", "Registro de cambios"),
        ("LICENSE", "Licencia del proyecto"),
        (".gitignore", "Archivos ignorados por Git"),
        (".env.example", "Ejemplo de configuración"),
    ]
    
    for file_path, description in main_files:
        total_checks += 1
        if check_file_exists(file_path, description):
            passed_checks += 1
    
    # 2. Verificar estructura de directorios
    print_header("ESTRUCTURA DE DIRECTORIOS")
    
    main_dirs = [
        ("docs", "Documentación"),
        ("scripts", "Scripts de utilidad"),
        ("templates", "Plantillas HTML"),
        ("static", "Archivos estáticos"),
        ("media", "Archivos de usuario"),
        ("usuarios", "Módulo de usuarios"),
        ("clientes", "Módulo de clientes"),
        ("productos", "Módulo de productos"),
        ("pedidos", "Módulo de pedidos"),
        ("notificaciones", "Módulo de notificaciones"),
        ("core", "Módulo central"),
        ("rpgestor20", "Configuración de Django"),
    ]
    
    for dir_path, description in main_dirs:
        total_checks += 1
        if check_directory_exists(dir_path, description):
            passed_checks += 1
    
    # 3. Verificar documentación
    print_header("DOCUMENTACIÓN")
    
    doc_files = [
        ("docs/INSTALACION.md", "Guía de instalación"),
        ("docs/DESPLIEGUE.md", "Guía de despliegue"),
        ("docs/API.md", "Documentación de API"),
        ("docs/MODULOS.md", "Documentación de módulos"),
        ("scripts/README.md", "Documentación de scripts"),
    ]
    
    for file_path, description in doc_files:
        total_checks += 1
        if check_file_exists(file_path, description):
            passed_checks += 1
    
    # 4. Verificar scripts organizados
    print_header("SCRIPTS DE UTILIDAD")
    
    script_files = [
        ("scripts/run_dev.py", "Servidor de desarrollo"),
        ("scripts/run_local_network.py", "Servidor de red local"),
        ("scripts/check_setup.py", "Verificación de configuración"),
        ("scripts/test_dashboard.py", "Test del dashboard"),
        ("scripts/network_utils.py", "Utilidades de red"),
    ]
    
    for file_path, description in script_files:
        total_checks += 1
        if check_file_exists(file_path, description):
            passed_checks += 1
    
    # 5. Verificar módulos de Django
    print_header("MÓDULOS DE DJANGO")
    
    django_modules = [
        "usuarios",
        "clientes", 
        "productos",
        "pedidos",
        "notificaciones",
        "core",
        "insights"
    ]
    
    for module in django_modules:
        total_checks += 1
        if check_python_module(module):
            passed_checks += 1
    
    # 6. Verificar archivos de configuración
    print_header("ARCHIVOS DE CONFIGURACIÓN")
    
    config_files = [
        ("rpgestor20/settings.py", "Configuración de Django"),
        ("rpgestor20/urls.py", "URLs principales"),
        ("rpgestor20/wsgi.py", "Configuración WSGI"),
        ("rpgestor20/asgi.py", "Configuración ASGI"),
        ("package.json", "Configuración de Node.js"),
        ("tailwind.config.js", "Configuración de Tailwind"),
    ]
    
    for file_path, description in config_files:
        total_checks += 1
        if check_file_exists(file_path, description):
            passed_checks += 1
    
    # 7. Verificar comandos de Django
    print_header("COMANDOS DE DJANGO")
    
    django_commands = [
        ("python manage.py check", "Verificación de Django"),
        ("python manage.py check --deploy", "Verificación para producción"),
    ]
    
    for command, description in django_commands:
        total_checks += 1
        if run_command(command, description):
            passed_checks += 1
    
    # 8. Verificar estructura de templates
    print_header("PLANTILLAS Y TEMPLATES")
    
    template_files = [
        ("templates/base.html", "Template base"),
        ("templates/menus/vendedor_menu.html", "Menú de vendedor"),
        ("templates/menus/jefe_ventas_menu.html", "Menú de jefe de ventas"),
        ("templates/menus/gestor_menu.html", "Menú de gestor"),
    ]
    
    for file_path, description in template_files:
        total_checks += 1
        if check_file_exists(file_path, description):
            passed_checks += 1
    
    # 9. Verificar archivos de datos
    print_header("DATOS Y EJEMPLOS")
    
    data_files = [
        ("docs/data", "Directorio de datos de ejemplo"),
        ("DOCUMENTOS", "Documentos de referencia"),
    ]
    
    for file_path, description in data_files:
        total_checks += 1
        if check_directory_exists(file_path, description):
            passed_checks += 1
    
    # Resumen final
    print_header("RESUMEN DE VERIFICACIÓN")
    
    success_rate = (passed_checks / total_checks) * 100
    
    print(f"📊 Verificaciones realizadas: {total_checks}")
    print(f"✅ Verificaciones exitosas: {passed_checks}")
    print(f"❌ Verificaciones fallidas: {total_checks - passed_checks}")
    print(f"📈 Tasa de éxito: {success_rate:.1f}%")
    
    if success_rate >= 95:
        print("\n🎉 ¡EXCELENTE! El proyecto está perfectamente organizado.")
        print("✨ RPGestor está listo para desarrollo y producción.")
    elif success_rate >= 85:
        print("\n👍 ¡BIEN! El proyecto está bien organizado.")
        print("🔧 Considera revisar los elementos faltantes.")
    elif success_rate >= 70:
        print("\n⚠️  El proyecto está parcialmente organizado.")
        print("🛠️  Se recomienda completar la organización.")
    else:
        print("\n❌ El proyecto necesita más organización.")
        print("🚨 Revisa los elementos faltantes antes de continuar.")
    
    # Recomendaciones finales
    print_header("RECOMENDACIONES FINALES")
    
    print("📋 Para completar la configuración:")
    print("   1. Copia .env.example a .env y configura tus variables")
    print("   2. Ejecuta: python manage.py migrate")
    print("   3. Crea un superusuario: python manage.py createsuperuser")
    print("   4. Ejecuta el servidor: python scripts/run_dev.py")
    print("   5. Visita: http://localhost:8000")
    
    print("\n📚 Documentación disponible:")
    print("   • README.md - Información general")
    print("   • docs/INSTALACION.md - Guía de instalación")
    print("   • docs/DESPLIEGUE.md - Guía de despliegue")
    print("   • docs/API.md - Documentación de API")
    print("   • docs/MODULOS.md - Descripción de módulos")
    
    print("\n🛠️  Scripts disponibles:")
    print("   • scripts/run_dev.py - Servidor de desarrollo")
    print("   • scripts/run_local_network.py - Servidor de red")
    print("   • scripts/check_setup.py - Verificar configuración")
    print("   • scripts/test_dashboard.py - Probar dashboard")
    
    return success_rate >= 85

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)