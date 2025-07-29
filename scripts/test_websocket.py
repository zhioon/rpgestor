#!/usr/bin/env python
"""
Script para probar las conexiones WebSocket
"""
import asyncio
import websockets
import json
import sys

async def test_websocket(url):
    """Prueba una conexión WebSocket"""
    print(f"Conectando a {url}...")
    
    try:
        async with websockets.connect(url) as websocket:
            print("✅ Conexión establecida!")
            
            # Esperar mensaje inicial
            response = await websocket.recv()
            print(f"📥 Mensaje recibido: {response}")
            
            # Enviar un mensaje de prueba
            test_message = {"message": "Hola, esto es una prueba"}
            print(f"📤 Enviando mensaje: {test_message}")
            await websocket.send(json.dumps(test_message))
            
            # Esperar respuesta
            response = await websocket.recv()
            print(f"📥 Respuesta recibida: {response}")
            
            # Mantener la conexión abierta por un momento
            print("⏳ Esperando mensajes por 10 segundos...")
            for i in range(10):
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    print(f"📥 Mensaje recibido: {response}")
                except asyncio.TimeoutError:
                    print(f"⏳ Esperando... {i+1}/10")
            
            print("✅ Prueba completada con éxito!")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    """Función principal"""
    print("🔌 PRUEBA DE WEBSOCKETS")
    print("=" * 50)
    
    # Obtener host y puerto de los argumentos o usar valores predeterminados
    host = "127.0.0.1"
    port = 8000
    
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    
    # URLs de WebSocket a probar
    urls = [
        f"ws://{host}:{port}/ws/notificaciones/",
        f"ws://{host}:{port}/ws/mensajes/"
    ]
    
    results = []
    
    for url in urls:
        print("\n" + "=" * 50)
        print(f"🔍 Probando: {url}")
        print("=" * 50)
        result = await test_websocket(url)
        results.append((url, result))
    
    print("\n" + "=" * 50)
    print("📊 RESULTADOS:")
    print("=" * 50)
    
    all_success = True
    for url, result in results:
        status = "✅ ÉXITO" if result else "❌ FALLO"
        print(f"{status} - {url}")
        if not result:
            all_success = False
    
    if all_success:
        print("\n🎉 Todas las conexiones WebSocket funcionan correctamente!")
    else:
        print("\n⚠️  Algunas conexiones WebSocket fallaron.")
    
    return 0 if all_success else 1

if __name__ == "__main__":
    asyncio.run(main())