# 🔌 Documentación de API - RPGestor

RPGestor incluye una API REST completa para integración con sistemas externos y desarrollo de aplicaciones móviles.

## 🚀 Información General

### Base URL
```
http://localhost:8000/api/v1/
https://tu-dominio.com/api/v1/
```

### Autenticación
La API utiliza autenticación basada en tokens JWT.

```http
Authorization: Bearer <tu_token_jwt>
```

### Formato de Respuesta
Todas las respuestas están en formato JSON:

```json
{
    "success": true,
    "data": {...},
    "message": "Operación exitosa",
    "timestamp": "2025-07-29T10:30:00Z"
}
```

## 🔐 Autenticación

### Obtener Token
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "tu_usuario",
    "password": "tu_password"
}
```

**Respuesta:**
```json
{
    "success": true,
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user": {
            "id": 1,
            "username": "vendedor1",
            "email": "vendedor1@example.com",
            "role": "Vendedor"
        }
    }
}
```

### Refrescar Token
```http
POST /api/auth/refresh/
Content-Type: application/json

{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 👥 Usuarios

### Obtener Perfil Actual
```http
GET /api/usuarios/me/
Authorization: Bearer <token>
```

### Actualizar Perfil
```http
PUT /api/usuarios/me/
Authorization: Bearer <token>
Content-Type: application/json

{
    "first_name": "Juan",
    "last_name": "Pérez",
    "email": "juan.perez@example.com"
}
```

### Cambiar Contraseña
```http
POST /api/usuarios/change-password/
Authorization: Bearer <token>
Content-Type: application/json

{
    "old_password": "password_actual",
    "new_password": "nuevo_password"
}
```

## 👤 Clientes

### Listar Clientes
```http
GET /api/clientes/
Authorization: Bearer <token>

# Parámetros de consulta opcionales:
# ?search=nombre_cliente
# ?page=1
# ?page_size=20
# ?favorito=true
```

**Respuesta:**
```json
{
    "success": true,
    "data": {
        "count": 150,
        "next": "http://localhost:8000/api/clientes/?page=2",
        "previous": null,
        "results": [
            {
                "id": 1,
                "nombre": "Cliente Ejemplo S.A.",
                "email": "contacto@cliente.com",
                "telefono": "+57 300 123 4567",
                "direccion": "Calle 123 #45-67",
                "ciudad": "Bogotá",
                "es_favorito": true,
                "fecha_creacion": "2025-01-15T10:30:00Z"
            }
        ]
    }
}
```

### Obtener Cliente Específico
```http
GET /api/clientes/{id}/
Authorization: Bearer <token>
```

### Crear Cliente
```http
POST /api/clientes/
Authorization: Bearer <token>
Content-Type: application/json

{
    "nombre": "Nuevo Cliente S.A.",
    "email": "nuevo@cliente.com",
    "telefono": "+57 300 123 4567",
    "direccion": "Calle 123 #45-67",
    "ciudad": "Medellín"
}
```

### Marcar como Favorito
```http
POST /api/clientes/{id}/toggle-favorito/
Authorization: Bearer <token>
```

## 📦 Productos

### Listar Productos
```http
GET /api/productos/
Authorization: Bearer <token>

# Parámetros opcionales:
# ?search=nombre_producto
# ?grupo=1
# ?subgrupo=2
# ?disponible=true
# ?page=1
```

**Respuesta:**
```json
{
    "success": true,
    "data": {
        "results": [
            {
                "id": 1,
                "codigo": "PROD001",
                "nombre": "Producto Ejemplo",
                "descripcion": "Descripción del producto",
                "precio": "25000.00",
                "stock": 100,
                "grupo": {
                    "id": 1,
                    "nombre": "Grupo A"
                },
                "subgrupo": {
                    "id": 1,
                    "nombre": "Subgrupo 1"
                },
                "imagen": "http://localhost:8000/media/productos/imagen.jpg"
            }
        ]
    }
}
```

### Obtener Producto Específico
```http
GET /api/productos/{id}/
Authorization: Bearer <token>
```

### Calcular Precio
```http
POST /api/productos/calcular-precio/
Authorization: Bearer <token>
Content-Type: application/json

{
    "producto_id": 1,
    "cantidad": 10,
    "descuento": 5.0
}
```

## 🛒 Pedidos

### Listar Pedidos
```http
GET /api/pedidos/
Authorization: Bearer <token>

# Parámetros opcionales:
# ?estado=pendiente
# ?cliente=1
# ?fecha_desde=2025-01-01
# ?fecha_hasta=2025-12-31
```

**Respuesta:**
```json
{
    "success": true,
    "data": {
        "results": [
            {
                "id": 1,
                "numero_pedido": "PED-2025-001",
                "cliente": {
                    "id": 1,
                    "nombre": "Cliente Ejemplo S.A."
                },
                "vendedor": {
                    "id": 1,
                    "nombre": "Juan Vendedor"
                },
                "fecha": "2025-07-29",
                "estado": "pendiente",
                "subtotal": "100000.00",
                "descuento": "5000.00",
                "total": "95000.00",
                "items": [
                    {
                        "producto": {
                            "id": 1,
                            "nombre": "Producto A"
                        },
                        "cantidad": 5,
                        "precio_unitario": "20000.00",
                        "subtotal": "100000.00"
                    }
                ]
            }
        ]
    }
}
```

### Crear Pedido
```http
POST /api/pedidos/
Authorization: Bearer <token>
Content-Type: application/json

{
    "cliente_id": 1,
    "observaciones": "Pedido urgente",
    "items": [
        {
            "producto_id": 1,
            "cantidad": 5,
            "precio_unitario": "20000.00"
        },
        {
            "producto_id": 2,
            "cantidad": 3,
            "precio_unitario": "15000.00"
        }
    ]
}
```

### Actualizar Estado de Pedido
```http
PATCH /api/pedidos/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "estado": "enviado"
}
```

### Generar PDF del Pedido
```http
GET /api/pedidos/{id}/pdf/
Authorization: Bearer <token>
```

## 📊 Dashboard y Estadísticas

### Obtener Métricas del Dashboard
```http
GET /api/dashboard/metricas/
Authorization: Bearer <token>

# Parámetros opcionales:
# ?periodo=mes_actual
# ?vendedor_id=1
```

**Respuesta:**
```json
{
    "success": true,
    "data": {
        "ventas_totales": "1500000.00",
        "pedidos_totales": 45,
        "clientes_activos": 23,
        "productos_vendidos": 156,
        "cumplimiento_meta": 85.5,
        "crecimiento_mensual": 12.3,
        "top_productos": [
            {
                "producto": "Producto A",
                "cantidad_vendida": 50,
                "ingresos": "250000.00"
            }
        ],
        "ventas_por_dia": [
            {
                "fecha": "2025-07-29",
                "ventas": "45000.00"
            }
        ]
    }
}
```

### Obtener Reportes
```http
GET /api/reportes/ventas/
Authorization: Bearer <token>

# Parámetros:
# ?fecha_inicio=2025-01-01
# ?fecha_fin=2025-12-31
# ?vendedor_id=1
# ?formato=json|pdf|excel
```

## 📅 Agenda

### Obtener Eventos de Agenda
```http
GET /api/agenda/eventos/
Authorization: Bearer <token>

# Parámetros opcionales:
# ?fecha_inicio=2025-07-29
# ?fecha_fin=2025-08-05
# ?tipo=reunion
```

### Crear Evento
```http
POST /api/agenda/eventos/
Authorization: Bearer <token>
Content-Type: application/json

{
    "titulo": "Reunión con cliente",
    "descripcion": "Presentación de productos",
    "tipo": "reunion",
    "fecha_inicio": "2025-07-30T14:00:00Z",
    "fecha_fin": "2025-07-30T15:00:00Z",
    "cliente_id": 1,
    "ubicacion": "Oficina cliente"
}
```

### Marcar Evento como Completado
```http
POST /api/agenda/eventos/{id}/completar/
Authorization: Bearer <token>
```

## 💬 Mensajes

### Obtener Mensajes Recibidos
```http
GET /api/mensajes/inbox/
Authorization: Bearer <token>

# Parámetros opcionales:
# ?leido=false
# ?tipo=motivacional
# ?prioridad=alta
```

### Marcar Mensaje como Leído
```http
POST /api/mensajes/{id}/marcar-leido/
Authorization: Bearer <token>
```

### Enviar Mensaje (Solo Jefe de Ventas)
```http
POST /api/mensajes/enviar/
Authorization: Bearer <token>
Content-Type: application/json

{
    "vendedor_id": 1,
    "tipo": "motivacional",
    "prioridad": "media",
    "asunto": "¡Excelente trabajo!",
    "mensaje": "Felicitaciones por superar la meta del mes."
}
```

## 🔔 Notificaciones

### Obtener Notificaciones
```http
GET /api/notificaciones/
Authorization: Bearer <token>

# Parámetros opcionales:
# ?leida=false
# ?tipo=pedido
```

### Marcar Notificación como Leída
```http
POST /api/notificaciones/{id}/marcar-leida/
Authorization: Bearer <token>
```

### Obtener Contador de Notificaciones
```http
GET /api/notificaciones/count/
Authorization: Bearer <token>
```

## 📱 WebSocket API

### Conexión WebSocket
```javascript
// Conectar a WebSocket
const socket = new WebSocket('ws://localhost:8000/ws/notificaciones/');

// Autenticación
socket.onopen = function(e) {
    socket.send(JSON.stringify({
        'type': 'authenticate',
        'token': 'tu_token_jwt'
    }));
};

// Recibir mensajes
socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('Notificación recibida:', data);
};
```

### Tipos de Mensajes WebSocket

#### Notificaciones
```json
{
    "type": "notification",
    "data": {
        "id": 1,
        "titulo": "Nuevo pedido",
        "mensaje": "Se ha creado un nuevo pedido #PED-2025-001",
        "tipo": "pedido",
        "timestamp": "2025-07-29T10:30:00Z"
    }
}
```

#### Mensajes
```json
{
    "type": "message",
    "data": {
        "id": 1,
        "remitente": "Jefe de Ventas",
        "asunto": "Reunión de equipo",
        "mensaje": "Reunión mañana a las 9:00 AM",
        "prioridad": "alta",
        "timestamp": "2025-07-29T10:30:00Z"
    }
}
```

## 🔍 Filtros y Búsqueda

### Parámetros de Filtrado Comunes
- `search` - Búsqueda por texto
- `page` - Número de página
- `page_size` - Elementos por página (máximo 100)
- `ordering` - Ordenamiento (`-fecha` para descendente)

### Ejemplos de Búsqueda Avanzada
```http
# Buscar productos por nombre y grupo
GET /api/productos/?search=producto&grupo=1&ordering=-fecha_creacion

# Filtrar pedidos por rango de fechas
GET /api/pedidos/?fecha_desde=2025-01-01&fecha_hasta=2025-12-31&estado=enviado

# Buscar clientes favoritos en una ciudad
GET /api/clientes/?favorito=true&ciudad=Bogotá&search=empresa
```

## ❌ Códigos de Error

### Códigos HTTP Estándar
- `200` - OK
- `201` - Creado
- `400` - Solicitud incorrecta
- `401` - No autorizado
- `403` - Prohibido
- `404` - No encontrado
- `500` - Error interno del servidor

### Formato de Error
```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Los datos proporcionados no son válidos",
        "details": {
            "email": ["Este campo es requerido"],
            "telefono": ["Formato de teléfono inválido"]
        }
    },
    "timestamp": "2025-07-29T10:30:00Z"
}
```

## 📝 Ejemplos de Integración

### JavaScript/React
```javascript
// Cliente API para RPGestor
class RPGestorAPI {
    constructor(baseURL, token) {
        this.baseURL = baseURL;
        this.token = token;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        const response = await fetch(url, config);
        return response.json();
    }

    // Obtener clientes
    async getClientes(params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.request(`/clientes/?${query}`);
    }

    // Crear pedido
    async crearPedido(pedidoData) {
        return this.request('/pedidos/', {
            method: 'POST',
            body: JSON.stringify(pedidoData)
        });
    }
}

// Uso
const api = new RPGestorAPI('http://localhost:8000/api/v1', 'tu_token');
const clientes = await api.getClientes({ search: 'empresa' });
```

### Python
```python
import requests

class RPGestorAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def get_clientes(self, **params):
        response = requests.get(
            f'{self.base_url}/clientes/',
            headers=self.headers,
            params=params
        )
        return response.json()

    def crear_pedido(self, pedido_data):
        response = requests.post(
            f'{self.base_url}/pedidos/',
            headers=self.headers,
            json=pedido_data
        )
        return response.json()

# Uso
api = RPGestorAPI('http://localhost:8000/api/v1', 'tu_token')
clientes = api.get_clientes(search='empresa')
```

## 🔧 Rate Limiting

La API implementa límites de velocidad:
- **Usuarios autenticados**: 1000 requests/hora
- **Usuarios anónimos**: 100 requests/hora

Headers de respuesta:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1627834800
```

## 📚 Recursos Adicionales

- **Postman Collection**: [Descargar colección](docs/postman/RPGestor_API.json)
- **OpenAPI Schema**: [Ver esquema](http://localhost:8000/api/schema/)
- **Swagger UI**: [Documentación interactiva](http://localhost:8000/api/docs/)

¡La API de RPGestor está lista para integrar con cualquier sistema! 🚀