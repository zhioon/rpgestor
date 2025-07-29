#!/usr/bin/env python
"""
Script para probar el envío de correos reales
Ejecutar con: python test_email.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpgestor20.settings')
django.setup()

from django.core.mail import EmailMessage
from django.conf import settings

def test_email():
    """Prueba el envío de un correo real"""
    
    print("🧪 Probando configuración de email...")
    print(f"📧 Backend: {settings.EMAIL_BACKEND}")
    print(f"🌐 Host: {settings.EMAIL_HOST}")
    print(f"🔌 Puerto: {settings.EMAIL_PORT}")
    print(f"👤 Usuario: {settings.EMAIL_HOST_USER}")
    print(f"📤 From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"🎯 Gestor: {settings.GESTOR_EMAIL}")
    print("-" * 50)
    
    try:
        # Crear mensaje de prueba
        msg = EmailMessage(
            subject='🧪 Prueba de RPGestor - Configuración de Email',
            body='''
¡Hola!

Este es un correo de prueba para verificar que la configuración de email de RPGestor funciona correctamente.

✅ Si recibes este correo, la configuración está funcionando perfectamente.

Detalles técnicos:
- Sistema: RPGestor 2.0
- Backend: Django Email
- Fecha: Ahora mismo
- Propósito: Verificación de configuración

¡Excelente! Ya puedes enviar correos reales desde RPGestor.

Saludos,
Sistema RPGestor
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.GESTOR_EMAIL],  # Se envía al gestor como prueba
        )
        
        print("📤 Enviando correo de prueba...")
        msg.send()
        print("✅ ¡Correo enviado exitosamente!")
        print(f"📬 Revisa la bandeja de entrada de: {settings.GESTOR_EMAIL}")
        
    except Exception as e:
        print("❌ Error al enviar correo:")
        print(f"   {str(e)}")
        print("\n🔧 Posibles soluciones:")
        print("   1. Verifica que el email y contraseña sean correctos")
        print("   2. Si usas Gmail, asegúrate de usar App Password")
        print("   3. Verifica que la verificación en 2 pasos esté habilitada")
        print("   4. Revisa la configuración del servidor SMTP")

if __name__ == '__main__':
    test_email()