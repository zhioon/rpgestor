# 📦 Documentación de Módulos - RPGestor

Esta documentación describe cada módulo del sistema RPGestor y sus funcionalidades.

## 🏗️ Arquitectura General

RPGestor está construido con una arquitectura modular que permite escalabilidad y mantenimiento fácil:

```
RPGestor/
├── 🏢 core/              # Funcionalidades centrales
├── 👥 usuarios/          # Gestión de usuarios y autenticación
├── 👤 clientes/          # Gestión de clientes
├── 📦 productos/         # Gestión de productos e inventario
├── 🛒 pedidos/           # Gestión de pedidos y ventas
├── 🔔 notificaciones/    # Sistema de notificaciones
└── 📊 insights/          # Reportes y análisis
```

## 🏢 Módulo Core

### Propósito
Contiene las funcionalidades centrales y compartidas del sistema.

### Componentes Principales
- **TimeStampedModel**: Modelo base con campos de fecha de creación y modificación
- **Utilidades**: Funciones helper compartidas
- **Vistas de error**: Manejo centralizado de errores
- **Middleware**: Procesamiento de requests

### Archivos Importantes
```
core/
├── models.py          # Modelos base
├── utils.py           # Utilidades compartidas
├── error_views.py     # Vistas de error personalizadas
└── management/        # Comandos de Django personalizados
```

### Funcionalidades
- ✅ Modelo base con timestamps automáticos
- ✅ Utilidades para formateo de datos
- ✅ Manejo de errores 404, 500, etc.
- ✅ Comandos personalizados de Django

---

## 👥 Módulo Usuarios

### Propósito
Gestión completa de usuarios, autenticación, perfiles y roles.

### Modelos Principales
- **User**: Usuario base de Django (extendido)
- **Vendedor**: Perfil de vendedor con presupuestos
- **UserProfile**: Perfil extendido con foto y datos adicionales
- **MensajeJefeVentas**: Mensajes internos del equipo
- **MetaVendedor**: Metas asignadas a vendedores
- **PresupuestoMensual**: Presupuestos específicos por mes
- **EventoAgenda**: Eventos de calendario

### Roles del Sistema
1. **👔 Gestor**: Acceso completo al sistema
2. **👨‍💼 Jefe de Ventas**: Gestión del equipo de ventas
3. **💼 Vendedor**: Gestión de clientes y pedidos

### Funcionalidades por Rol

#### Gestor
- ✅ Dashboard general con métricas globales
- ✅ Gestión de todos los pedidos
- ✅ Administración de inventario completo
- ✅ Configuración del sistema
- ✅ Acceso a todos los reportes

#### Jefe de Ventas
- ✅ Dashboard del equipo de ventas
- ✅ Gestión de vendedores
- ✅ Asignación de metas y presupuestos
- ✅ Envío de mensajes al equipo
- ✅ Reportes de rendimiento
- ✅ Agenda y reuniones

#### Vendedor
- ✅ Dashboard personal
- ✅ Gestión de clientes asignados
- ✅ Creación y seguimiento de pedidos
- ✅ Agenda personal
- ✅ Recepción de mensajes
- ✅ Calculadora de precios

### Vistas Principales
```
usuarios/
├── views.py                    # Dashboards principales
├── profile_views.py            # Gestión de perfiles
├── agenda_views.py             # Sistema de agenda
├── inbox_views.py              # Sistema de mensajes
├── jefe_ventas_views.py        # Funcionalidades de jefe
├── calculadora_views.py        # Calculadora de precios
└── notification_views.py       # Notificaciones
```

---

## 👤 Módulo Clientes

### Propósito
Gestión completa de la base de datos de clientes.

### Modelo Principal
- **Cliente**: Información completa del cliente

### Funcionalidades
- ✅ **Lista de clientes** con búsqueda y filtros
- ✅ **Clientes favoritos** para acceso rápido
- ✅ **Historial de pedidos** por cliente
- ✅ **Información de contacto** completa
- ✅ **Notas y observaciones** personalizadas
- ✅ **Importación masiva** desde Excel

### Campos del Cliente
```python
- nombre: Nombre o razón social
- email: Correo electrónico
- telefono: Número de contacto
- direccion: Dirección física
- ciudad: Ciudad de ubicación
- vendedor: Vendedor asignado
- es_favorito: Marcador de favorito
- notas: Observaciones adicionales
```

### Vistas Disponibles
- **Lista de clientes**: Vista principal con filtros
- **Detalle de cliente**: Información completa
- **Clientes favoritos**: Acceso rápido
- **Crear/Editar cliente**: Formularios de gestión

---

## 📦 Módulo Productos

### Propósito
Gestión del inventario y catálogo de productos.

### Modelos Principales
- **Grupo**: Categorías principales de productos
- **SubGrupo**: Subcategorías de productos
- **Producto**: Información completa del producto

### Funcionalidades
- ✅ **Inventario completo** con stock en tiempo real
- ✅ **Categorización** por grupos y subgrupos
- ✅ **Calculadora de precios** integrada
- ✅ **Importación masiva** desde Excel
- ✅ **Gestión de imágenes** de productos
- ✅ **Control de stock** y alertas

### Estructura de Productos
```
Grupo (ej: Medicamentos)
└── SubGrupo (ej: Analgésicos)
    └── Producto (ej: Acetaminofén 500mg)
```

### Campos del Producto
```python
- codigo: Código único del producto
- nombre: Nombre del producto
- descripcion: Descripción detallada
- precio: Precio base
- stock: Cantidad disponible
- grupo: Categoría principal
- subgrupo: Subcategoría
- imagen: Imagen del producto
- activo: Estado del producto
```

### Vistas por Rol
- **Gestor**: Inventario completo, importación masiva
- **Jefe de Ventas**: Vista de inventario del equipo
- **Vendedor**: Inventario personal asignado

---

## 🛒 Módulo Pedidos

### Propósito
Gestión completa del proceso de ventas y pedidos.

### Modelos Principales
- **Pedido**: Información principal del pedido
- **ItemPedido**: Productos incluidos en el pedido

### Estados del Pedido
1. **📝 Borrador**: En proceso de creación
2. **⏳ Pendiente**: Esperando procesamiento
3. **✅ Confirmado**: Confirmado por el cliente
4. **📦 Enviado**: En proceso de entrega
5. **🎉 Finalizado**: Entregado exitosamente
6. **❌ Cancelado**: Cancelado por alguna razón

### Funcionalidades
- ✅ **Creación de pedidos** con interfaz intuitiva
- ✅ **Cálculo automático** de totales y descuentos
- ✅ **Seguimiento de estados** del pedido
- ✅ **Generación de PDFs** para impresión
- ✅ **Historial completo** de cambios
- ✅ **Notificaciones automáticas** de cambios de estado

### Campos del Pedido
```python
- numero_pedido: Número único autogenerado
- cliente: Cliente asociado
- vendedor: Vendedor responsable
- fecha: Fecha de creación
- estado: Estado actual
- subtotal: Suma de items
- descuento: Descuento aplicado
- total: Total final
- observaciones: Notas adicionales
```

### Proceso de Creación
1. **Seleccionar cliente** de la lista
2. **Agregar productos** con cantidades
3. **Aplicar descuentos** si corresponde
4. **Revisar totales** calculados automáticamente
5. **Guardar pedido** y generar número único
6. **Generar PDF** para entrega

---

## 🔔 Módulo Notificaciones

### Propósito
Sistema de notificaciones en tiempo real para todos los usuarios.

### Modelos Principales
- **Notificacion**: Notificaciones del sistema

### Tipos de Notificaciones
- **📦 Pedido**: Nuevos pedidos, cambios de estado
- **👤 Cliente**: Nuevos clientes, actualizaciones
- **📊 Meta**: Cumplimiento de objetivos
- **💬 Mensaje**: Mensajes internos
- **⚠️ Sistema**: Alertas del sistema

### Funcionalidades
- ✅ **Notificaciones en tiempo real** con WebSockets
- ✅ **Centro de notificaciones** unificado
- ✅ **Filtros por tipo** y estado
- ✅ **Marcado como leída** individual y masivo
- ✅ **Notificaciones push** (futuro)

### Canales de Entrega
1. **WebSocket**: Tiempo real en la aplicación
2. **Email**: Notificaciones importantes
3. **Base de datos**: Historial persistente

---

## 📊 Módulo Insights

### Propósito
Reportes, análisis y métricas del negocio.

### Funcionalidades
- ✅ **Reportes de ventas** por período
- ✅ **Análisis de rendimiento** por vendedor
- ✅ **Métricas de productos** más vendidos
- ✅ **Análisis de clientes** más activos
- ✅ **Gráficos interactivos** con Chart.js
- ✅ **Exportación** a PDF y Excel

### Tipos de Reportes
1. **Ventas por período**: Diario, semanal, mensual, anual
2. **Rendimiento de vendedores**: Comparativas y rankings
3. **Productos top**: Más vendidos y rentables
4. **Análisis de clientes**: Frecuencia y valor
5. **Cumplimiento de metas**: Progreso vs objetivos

---

## 🔄 Integración entre Módulos

### Flujo Principal
```
Cliente → Producto → Pedido → Notificación → Reporte
   ↓         ↓         ↓          ↓           ↓
Usuario → Inventario → Venta → Dashboard → Insights
```

### Dependencias
- **Pedidos** depende de **Clientes** y **Productos**
- **Notificaciones** se integra con todos los módulos
- **Insights** consume datos de todos los módulos
- **Usuarios** gestiona permisos para todos los módulos

### Comunicación entre Módulos
- **Signals de Django**: Para eventos automáticos
- **WebSockets**: Para actualizaciones en tiempo real
- **Cache con Redis**: Para optimización de consultas
- **API REST**: Para integraciones externas

---

## 🛠️ Herramientas de Desarrollo

### Testing
Cada módulo incluye tests unitarios y de integración:
```bash
# Ejecutar tests de un módulo específico
python manage.py test usuarios
python manage.py test productos
python manage.py test pedidos
```

### Migraciones
Gestión de cambios en la base de datos:
```bash
# Crear migraciones para un módulo
python manage.py makemigrations usuarios

# Aplicar migraciones
python manage.py migrate
```

### Comandos Personalizados
Cada módulo puede incluir comandos de Django personalizados:
```bash
# Importar productos desde Excel
python manage.py import_productos archivo.xlsx

# Generar datos de prueba
python manage.py create_test_data

# Limpiar datos antiguos
python manage.py cleanup_old_data
```

---

## 📈 Escalabilidad

### Optimizaciones Implementadas
- **Select Related**: Para reducir consultas a la base de datos
- **Prefetch Related**: Para optimizar relaciones many-to-many
- **Cache con Redis**: Para consultas frecuentes
- **Paginación**: Para listas grandes de datos
- **Índices de base de datos**: Para búsquedas rápidas

### Futuras Mejoras
- **Microservicios**: Separar módulos en servicios independientes
- **API GraphQL**: Para consultas más eficientes
- **Cache distribuido**: Para múltiples servidores
- **Queue de tareas**: Para procesamiento asíncrono
- **CDN**: Para archivos estáticos y media

¡Cada módulo está diseñado para ser independiente pero integrado perfectamente con el resto del sistema! 🚀