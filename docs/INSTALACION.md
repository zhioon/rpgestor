# 📋 Guía de Instalación - RPGestor

Esta guía te llevará paso a paso por el proceso de instalación y configuración de RPGestor.

## 🔧 Prerrequisitos

### Software Requerido
- **Python 3.11+** - [Descargar Python](https://www.python.org/downloads/)
- **PostgreSQL 12+** - [Descargar PostgreSQL](https://www.postgresql.org/download/)
- **Redis 6+** - [Descargar Redis](https://redis.io/download)
- **Git** - [Descargar Git](https://git-scm.com/downloads)

### Opcional (Recomendado)
- **Node.js 16+** - Para desarrollo con Tailwind CSS
- **pgAdmin** - Para administración visual de PostgreSQL

## 🚀 Instalación Paso a Paso

### 1. Preparar el Entorno

```bash
# Clonar el repositorio
git clone <repository-url>
cd RPGestor_2_0

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 2. Instalar Dependencias

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt
```

### 3. Configurar Base de Datos

#### PostgreSQL
```bash
# Conectar a PostgreSQL como superusuario
psql -U postgres

# Crear base de datos
CREATE DATABASE rpgestor_db;

# Crear usuario (opcional)
CREATE USER rpgestor_user WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE rpgestor_db TO rpgestor_user;

# Salir de PostgreSQL
\q
```

### 4. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env
```

Editar el archivo `.env` con tus configuraciones:

```env
# Base de datos
DATABASE_URL=postgresql://rpgestor_user:tu_password_seguro@localhost:5432/rpgestor_db

# Django
SECRET_KEY=tu_clave_secreta_muy_segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Redis
REDIS_URL=redis://localhost:6379/0

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_password_de_aplicacion
EMAIL_USE_TLS=True
```

### 5. Ejecutar Migraciones

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### 6. Cargar Datos Iniciales (Opcional)

```bash
# Cargar datos de ejemplo
python manage.py loaddata fixtures/initial_data.json
```

### 7. Configurar Archivos Estáticos

```bash
# Recopilar archivos estáticos
python manage.py collectstatic --noinput
```

### 8. Iniciar Servicios

#### Terminal 1 - Redis
```bash
redis-server
```

#### Terminal 2 - Django
```bash
# Servidor básico
python manage.py runserver

# O usar script personalizado
python scripts/run_dev.py
```

## 🔧 Configuración Avanzada

### WebSockets (Tiempo Real)
Para funcionalidades en tiempo real como notificaciones:

```bash
# Instalar dependencias adicionales
pip install channels channels-redis

# Ejecutar con soporte WebSocket
python scripts/run_asgi.py
```

### Configuración de Red Local
Para acceder desde otros dispositivos en la red:

```bash
python scripts/run_local_network.py
```

### Configuración de Producción

#### 1. Variables de Entorno de Producción
```env
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
SECRET_KEY=clave_super_secreta_para_produccion
```

#### 2. Servidor Web
```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn rpgestor20.wsgi:application --bind 0.0.0.0:8000
```

#### 3. Servidor de Archivos Estáticos
Configurar Nginx o Apache para servir archivos estáticos.

## 🧪 Verificar Instalación

### 1. Ejecutar Tests
```bash
python -m pytest
```

### 2. Verificar Configuración
```bash
python scripts/check_setup.py
```

### 3. Probar Dashboard
```bash
python scripts/test_dashboard.py
```

## 🐛 Solución de Problemas

### Error de Base de Datos
```bash
# Verificar conexión a PostgreSQL
psql -U rpgestor_user -d rpgestor_db -h localhost

# Recrear migraciones si es necesario
python manage.py migrate --run-syncdb
```

### Error de Redis
```bash
# Verificar que Redis esté ejecutándose
redis-cli ping
# Debería responder: PONG
```

### Error de Permisos
```bash
# En Linux/Mac, dar permisos a scripts
chmod +x scripts/*.py
```

### Error de Dependencias
```bash
# Reinstalar dependencias
pip install --force-reinstall -r requirements.txt
```

## 📊 Datos de Prueba

### Crear Usuarios de Prueba
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User, Group
from usuarios.models import Vendedor

# Crear grupos
gestor_group, _ = Group.objects.get_or_create(name='Gestor')
jefe_group, _ = Group.objects.get_or_create(name='JefeVentas')
vendedor_group, _ = Group.objects.get_or_create(name='Vendedor')

# Crear usuario vendedor
user = User.objects.create_user('vendedor1', 'vendedor1@test.com', 'password123')
user.groups.add(vendedor_group)
Vendedor.objects.create(user=user, presupuesto=100000)

# Crear usuario jefe de ventas
jefe = User.objects.create_user('jefe1', 'jefe1@test.com', 'password123')
jefe.groups.add(jefe_group)
Vendedor.objects.create(user=jefe, presupuesto=0)
```

## 🎯 Próximos Pasos

1. **Acceder al Admin**: http://localhost:8000/admin/
2. **Dashboard Principal**: http://localhost:8000/
3. **Crear Productos**: Importar desde Excel en el admin
4. **Configurar Usuarios**: Asignar roles y permisos
5. **Probar Funcionalidades**: Crear pedidos, clientes, etc.

## 📞 Soporte

Si encuentras problemas durante la instalación:

1. Revisa los logs en la consola
2. Verifica que todos los servicios estén ejecutándose
3. Consulta la documentación específica de cada módulo
4. Contacta al equipo de soporte

¡Listo! RPGestor debería estar funcionando correctamente. 🎉