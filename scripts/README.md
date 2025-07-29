# Scripts de RPGestor

Esta carpeta contiene scripts utilitarios para el desarrollo y mantenimiento de RPGestor.

## Scripts Disponibles

### Desarrollo y Testing
- `run_dev.py` - Servidor de desarrollo
- `run_local_network.py` - Servidor para red local
- `run_network.py` - Servidor de red
- `run_asgi.py` - Servidor ASGI para WebSockets

### Configuración
- `server_config.py` - Configuración del servidor
- `network_utils.py` - Utilidades de red

### Testing y Diagnóstico
- `test_dashboard.py` - Pruebas del dashboard
- `test_dashboard_data.py` - Pruebas de datos del dashboard
- `test_email.py` - Pruebas de email
- `test_login_redirect.py` - Pruebas de redirección de login
- `test_simple_view.py` - Pruebas de vistas simples
- `test_websocket.py` - Pruebas de WebSockets
- `check_setup.py` - Verificación de configuración
- `diagnostico_dashboard.py` - Diagnóstico del dashboard
- `verificar_dashboard.py` - Verificación del dashboard

## Uso

Para ejecutar cualquier script:
```bash
python scripts/nombre_del_script.py
```

## Notas
- Todos los scripts deben ejecutarse desde la raíz del proyecto
- Asegúrate de tener el entorno virtual activado antes de ejecutar los scripts