#!/usr/bin/env python
"""
Script para generar una SECRET_KEY segura para Django
"""

import secrets
import string

def generate_secret_key(length=50):
    """Generar una clave secreta segura para Django"""
    # Caracteres seguros para SECRET_KEY
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secret_key

def main():
    print("🔐 Generador de SECRET_KEY para Django")
    print("="*50)
    
    # Generar varias opciones
    print("🎲 Aquí tienes 3 opciones de SECRET_KEY seguras:")
    print()
    
    for i in range(1, 4):
        key = generate_secret_key()
        print(f"Opción {i}:")
        print(f"SECRET_KEY={key}")
        print()
    
    print("📋 Instrucciones:")
    print("1. Copia una de las claves generadas arriba")
    print("2. En Railway, ve a Variables de entorno")
    print("3. Agrega: SECRET_KEY=la-clave-que-copiaste")
    print("4. ¡Nunca compartas esta clave con nadie!")
    print()
    print("⚠️  IMPORTANTE: Cada entorno (desarrollo, producción) debe tener su propia SECRET_KEY")

if __name__ == "__main__":
    main()