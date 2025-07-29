# 🚀 RPGestor - Sistema de Gestión de Ventas

RPGestor es un sistema completo de gestión de ventas desarrollado en Django, diseñado para optimizar la gestión de equipos de ventas, clientes, productos y pedidos.

## 📋 Características Principales

### 👥 Gestión de Usuarios
- **Roles diferenciados**: Vendedor, Jefe de Ventas, Gestor
- **Dashboards personalizados** para cada rol
- **Sistema de perfiles** con fotos y información personal
- **Autenticación segura** con django-allauth

### 📊 Dashboard Inteligente
- **Métricas en tiempo real** de ventas y rendimiento
- **Gráficos interactivos** con estadísticas detalladas
- **Indicadores de cumplimiento** de metas y presupuestos
- **Vista consolidada** del estado del negocio

### 🛒 Gestión de Pedidos
- **Creación de pedidos** con interfaz intuitiva
- **Seguimiento completo** del estado de pedidos
- **Cálculo automático** de precios y descuentos
- **Historial detallado** de transacciones

### 👤 Gestión de Clientes
- **Base de datos completa** de clientes
- **Clientes favoritos** para acceso rápido
- **Historial de pedidos** por cliente
- **Información de contacto** y preferencias

### 📦 Gestión de Productos
- **Inventario completo** con stock en tiempo real
- **Categorización** por grupos y subgrupos
- **Calculadora de precios** integrada
- **Importación masiva** desde Excel

### 📅 Sistema de Agenda
- **Calendario personal** para cada vendedor
- **Creación de reuniones** y citas
- **Recordatorios automáticos**
- **Gestión de eventos** del equipo

### 💬 Sistema de Mensajería
- **Mensajes internos** entre jefe y vendedores
- **Bandeja de entrada** organizada
- **Filtros y búsqueda** avanzada
- **Notificaciones en tiempo real**

### 🎯 Gestión de Metas
- **Asignación de presupuestos** mensuales
- **Seguimiento de cumplimiento** de metas
- **Reportes de rendimiento** individual y grupal
- **Alertas automáticas** de desviaciones

### 🔔 Sistema de Notificaciones
- **Notificaciones en tiempo real** con WebSockets
- **Alertas personalizadas** por rol
- **Centro de notificaciones** unificado

## 🛠️ Tecnologías Utilizadas

### Backend
- **Django 4.2.23** - Framework web principal
- **Django REST Framework** - API REST
- **Channels** - WebSockets para tiempo real
- **PostgreSQL** - Base de datos principal
- **Redis** - Cache y sesiones

### Frontend
- **HTML5/CSS3** - Estructura y estilos
- **Tailwind CSS** - Framework de estilos
- **JavaScript** - Interactividad
- **Chart.js** - Gráficos y visualizaciones

### Herramientas
- **Pandas** - Procesamiento de datos
- **OpenPyXL** - Manejo de archivos Excel
- **ReportLab** - Generación de PDFs
- **QRCode** - Generación de códigos QR

## 📁 Estructura del Proyecto

```
RPGestor_2_0/
├── 📁 clientes/          # Gestión de clientes
├── 📁 core/              # Funcionalidades centrales
├── 📁 pedidos/           # Gestión de pedidos
├── 📁 productos/         # Gestión de productos e inventario
├── 📁 usuarios/          # Gestión de usuarios y autenticación
├── 📁 notificaciones/    # Sistema de notificaciones
├── 📁 insights/          # Reportes y análisis
├── 📁 templates/         # Plantillas HTML
├── 📁 static/            # Archivos estáticos (CSS, JS, imágenes)
├── 📁 media/             # Archivos subidos por usuarios
├── 📁 scripts/           # Scripts de utilidad y testing
├── 📁 docs/              # Documentación y datos de ejemplo
├── 📁 DOCUMENTOS/        # Archivos Excel de referencia
└── 📁 rpgestor20/        # Configuración principal de Django
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.11+
- PostgreSQL 12+
- Redis 6+
- Node.js 16+ (para Tailwind CSS)

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd RPGestor_2_0
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
```bash
# Crear base de datos PostgreSQL
createdb rpgestor_db

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario
```bash
python manage.py createsuperuser
```

### 6. Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
```

### 7. Ejecutar servidor de desarrollo
```bash
# Servidor básico
python manage.py runserver

# Servidor con WebSockets
python scripts/run_dev.py

# Servidor para red local
python scripts/run_local_network.py
```

## 🔧 Scripts Disponibles

### Desarrollo
- `scripts/run_dev.py` - Servidor de desarrollo
- `scripts/run_local_network.py` - Servidor para red local
- `scripts/run_network.py` - Servidor de red
- `scripts/run_asgi.py` - Servidor ASGI para WebSockets

### Testing
- `scripts/test_dashboard.py` - Pruebas del dashboard
- `scripts/test_websocket.py` - Pruebas de WebSockets
- `scripts/check_setup.py` - Verificación de configuración

## 👥 Roles y Permisos

### 🏢 Gestor
- Acceso completo al sistema
- Gestión de todos los pedidos
- Administración de inventario
- Configuración del sistema

### 👔 Jefe de Ventas
- Gestión del equipo de ventas
- Asignación de metas y presupuestos
- Envío de mensajes al equipo
- Reportes de rendimiento
- Acceso a agenda y reuniones

### 💼 Vendedor
- Creación y gestión de pedidos
- Gestión de clientes asignados
- Acceso a inventario personal
- Agenda y calendario personal
- Recepción de mensajes

## 📊 Funcionalidades por Módulo

### Clientes
- ✅ Lista completa de clientes
- ✅ Clientes favoritos
- ✅ Historial de pedidos
- ✅ Información de contacto

### Pedidos
- ✅ Creación de pedidos
- ✅ Estados de pedido
- ✅ Cálculo de precios
- ✅ Generación de PDFs

### Productos
- ✅ Inventario completo
- ✅ Categorización
- ✅ Calculadora de precios
- ✅ Importación desde Excel

### Usuarios
- ✅ Gestión de perfiles
- ✅ Sistema de agenda
- ✅ Mensajería interna
- ✅ Notificaciones

## 🔒 Seguridad

- **Autenticación robusta** con django-allauth
- **Control de acceso** basado en roles
- **Protección CSRF** en todos los formularios
- **Validación de datos** en backend y frontend
- **Sesiones seguras** con Redis

## 📈 Rendimiento

- **Cache con Redis** para consultas frecuentes
- **Optimización de consultas** con select_related y prefetch_related
- **Compresión de archivos** estáticos
- **WebSockets** para actualizaciones en tiempo real

## 🐛 Testing

```bash
# Ejecutar todas las pruebas
python -m pytest

# Pruebas específicas
python scripts/test_dashboard.py
python scripts/test_websocket.py
```

## 📝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

Desarrollado con ❤️ para optimizar la gestión de ventas.

## 📞 Soporte

Para soporte técnico o consultas:
- 📧 Email: soporte@rpgestor.com
- 📱 WhatsApp: +57 XXX XXX XXXX
- 🌐 Web: www.rpgestor.com

---

⭐ Si este proyecto te ha sido útil, ¡no olvides darle una estrella!