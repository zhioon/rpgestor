# Guía del Servidor ASGI con Channels

## Problema Solucionado

Este proyecto tenía problemas para ejecutar WebSockets con Channels debido a:

1. **Django Runserver vs Channels ASGI**: `manage.py runserver` usa WSGI por defecto, no ASGI
2. **Importación temprana de módulos**: Los procesos hijos importaban módulos antes de cargar Django settings
3. **Multiproceso y recarga automática**: Los subprocesos no heredaban las variables de entorno
4. **Lugar de ejecución**: Ejecutar desde carpetas incorrectas causaba errores de importación

## Solución Implementada

### 1. ASGI Mejorado (`rpgestor20/asgi.py`)
- Configuración explícita de Django settings
- Llamada a `django.setup()` antes de importar modelos
- Manejo correcto del ProtocolTypeRouter

### 2. Scripts de Ejecución

#### Para Producción: `run_asgi.py`
```bash
python run_asgi.py
```
- Sin reload automático
- Configuración optimizada para producción
- Log level: info

#### Para Desarrollo: `run_dev.py`
```bash
python run_dev.py
```
- Con reload automático
- Configuración optimizada para desarrollo
- Log level: debug
- Excluye archivos innecesarios del reload

#### Comando Django: `manage.py runasgi`
```bash
python manage.py runasgi
python manage.py runasgi --reload
python manage.py runasgi --host 0.0.0.0 --port 8080
```

### 3. Configuración Centralizada (`server_config.py`)
- Configuraciones para diferentes entornos
- Fácil mantenimiento y modificación
- Información clara del servidor

## Cómo Usar

### 🚀 Scripts Principales (Interactivos)

#### 🔧 Desarrollo (Recomendado)
```bash
python run_dev.py
```
- Te pregunta: ¿Solo local o acceso desde red?
- Detecta automáticamente tu IP
- Reload automático activado
- Logs detallados para debugging

#### 🚀 Producción
```bash
python run_asgi.py
```
- Te pregunta: ¿Solo local o acceso desde red?
- Detecta automáticamente tu IP
- Sin reload (más estable y rápido)
- Logs optimizados

### 🌐 Scripts de Red Rápidos (Sin preguntas)

#### Red Local Automática (¡SÚPER FÁCIL!)
```bash
python run_network.py
```
- ✅ Detecta tu IP automáticamente
- ✅ Permite conexiones desde móviles/tablets/otras PCs
- ✅ Perfecto para testing con otros dispositivos
- ✅ Reload automático

#### Solo Localhost (Privado)
```bash
python run_local_network.py
```
- ✅ Solo accesible desde tu computadora
- ✅ Más seguro para desarrollo privado
- ✅ Reload automático

### ⚙️ Comando Django (Máxima Flexibilidad)

#### Opciones básicas:
```bash
# Interactivo (te pregunta local o red):
python manage.py runasgi

# Forzar acceso desde red:
python manage.py runasgi --network

# Solo localhost:
python manage.py runasgi --localhost

# Con reload automático:
python manage.py runasgi --network --reload
```

#### Opciones avanzadas:
```bash
# Puerto personalizado:
python manage.py runasgi --network --port 3000

# Host específico:
python manage.py runasgi --host 192.168.1.100

# Ver interfaces de red disponibles:
python manage.py runasgi --show-interfaces
```

### 🔍 Utilidades de Red

#### Ver tu IP actual:
```bash
python -c "from network_utils import get_local_ip; print(f'Tu IP: {get_local_ip()}')"
```

#### Ver todas las interfaces de red:
```bash
python -c "from network_utils import get_network_interfaces_summary; get_network_interfaces_summary()"
```

## URLs Disponibles

### 🏠 Acceso Local (solo tu computadora):
- **HTTP**: http://127.0.0.1:8000/
- **WebSocket Notificaciones**: ws://127.0.0.1:8000/ws/notificaciones/
- **WebSocket Mensajes**: ws://127.0.0.1:8000/ws/mensajes/

### 🌐 Acceso de Red (otros dispositivos):
Cuando uses `run_local_network.py` o `--network`:
- **HTTP**: http://[TU_IP_LOCAL]:8000/
- **WebSocket Notificaciones**: ws://[TU_IP_LOCAL]:8000/ws/notificaciones/
- **WebSocket Mensajes**: ws://[TU_IP_LOCAL]:8000/ws/mensajes/

*La IP exacta se mostrará automáticamente al ejecutar el servidor*

## Requisitos

Asegúrate de tener instalado:

```bash
pip install uvicorn
pip install channels
pip install channels-redis
```

## Verificación

Para verificar que todo funciona:

1. Inicia el servidor con cualquiera de los métodos
2. Ve a tu aplicación web
3. Abre las herramientas de desarrollador del navegador
4. Verifica que las conexiones WebSocket se establezcan correctamente

## Troubleshooting

### Error: "Apps aren't loaded yet"
- **Causa**: Django no se configuró correctamente antes de importar modelos
- **Solución**: Ya está solucionado en el nuevo `asgi.py`

### Error: "No module named 'rpgestor20'"
- **Causa**: Ejecutar desde la carpeta incorrecta
- **Solución**: Ejecutar desde la raíz del proyecto (donde está `manage.py`)

### Error: WebSockets no funcionan
- **Causa**: Usar `manage.py runserver` en lugar de ASGI
- **Solución**: Usar uno de los scripts proporcionados

### Error: "uvicorn not found"
- **Causa**: uvicorn no está instalado
- **Solución**: `pip install uvicorn`

### Error: No puedo conectar desde mi móvil/tablet
- **Causa**: Firewall de Windows bloqueando conexiones
- **Solución**: 
  1. Ve a "Configuración de Windows Defender Firewall"
  2. Permite Python.exe en redes privadas
  3. O temporalmente desactiva el firewall para testing

### Error: "Connection refused" desde otros dispositivos
- **Causa**: No estás usando el modo de red o IP incorrecta
- **Solución**: 
  1. Usa `python run_network.py` o `--network`
  2. Verifica que estés en la misma red WiFi
  3. Usa la IP que muestra el servidor, no localhost

### Error: El servidor se reinicia constantemente
- **Causa**: Reload automático detectando cambios innecesarios
- **Solución**: Usa `python run_asgi.py` (sin reload) para producción

## Notas Importantes

1. **No uses `manage.py runserver`** para WebSockets - usa los scripts ASGI
2. **Para desarrollo** usa `run_dev.py` (con reload)
3. **Para producción** usa `run_asgi.py` (sin reload)
4. **Redis debe estar ejecutándose** para que funcionen las notificaciones
5. **Ejecuta siempre desde la raíz del proyecto** (donde está `manage.py`)

## Estructura de Archivos Creados/Modificados

```
├── rpgestor20/
│   └── asgi.py                     # ✅ Mejorado con django.setup()
├── notificaciones/
│   └── routing.py                  # ✅ Corregido patrones WebSocket
├── core/
│   └── management/
│       ├── __init__.py             # ✅ Nuevo
│       └── commands/
│           ├── __init__.py         # ✅ Nuevo
│           └── runasgi.py          # ✅ Comando Django con detección de IP
├── run_asgi.py                     # ✅ Mejorado con detección automática de IP
├── run_dev.py                      # ✅ Mejorado con opciones de red
├── run_network.py                  # ✅ Nuevo - Acceso automático desde red local
├── run_local_network.py            # ✅ Nuevo - Solo localhost
├── server_config.py                # ✅ Configuración centralizada
├── network_utils.py                # ✅ Utilidades de detección de IP y red
├── check_setup.py                  # ✅ Script de verificación mejorado
└── README_SERVIDOR.md              # ✅ Esta guía completa
```

### 📋 Resumen de Funcionalidades por Archivo:

- **`network_utils.py`**: Detecta IP automáticamente, maneja interfaces de red
- **`run_network.py`**: Acceso rápido desde red local (móviles, tablets)
- **`run_local_network.py`**: Acceso solo desde localhost (privado)
- **`run_dev.py`** y **`run_asgi.py`**: Ahora preguntan si quieres red local o solo localhost
- **`manage.py runasgi`**: Comando Django con todas las opciones de red