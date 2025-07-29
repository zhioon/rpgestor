# 🚀 Guía de Despliegue - RPGestor

Esta guía cubre el despliegue de RPGestor en diferentes entornos de producción.

## 🎯 Opciones de Despliegue

### 1. Servidor VPS/Dedicado
- **Control completo** del servidor
- **Configuración personalizada**
- **Escalabilidad manual**

### 2. Plataformas Cloud
- **Heroku** - Fácil despliegue
- **DigitalOcean App Platform** - Escalable
- **AWS/GCP/Azure** - Empresarial

### 3. Contenedores
- **Docker** - Portabilidad
- **Kubernetes** - Orquestación

## 🖥️ Despliegue en VPS/Servidor Dedicado

### Prerrequisitos del Servidor
```bash
# Ubuntu 20.04+ / CentOS 8+
# Mínimo 2GB RAM, 20GB almacenamiento
# Python 3.11+, PostgreSQL 12+, Redis 6+, Nginx
```

### 1. Preparar el Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
sudo apt install -y python3.11 python3.11-venv python3-pip
sudo apt install -y postgresql postgresql-contrib
sudo apt install -y redis-server
sudo apt install -y nginx
sudo apt install -y git curl
```

### 2. Configurar PostgreSQL

```bash
# Cambiar a usuario postgres
sudo -u postgres psql

# Crear base de datos y usuario
CREATE DATABASE rpgestor_prod;
CREATE USER rpgestor_user WITH PASSWORD 'password_super_seguro';
ALTER ROLE rpgestor_user SET client_encoding TO 'utf8';
ALTER ROLE rpgestor_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE rpgestor_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE rpgestor_prod TO rpgestor_user;
\q

# Configurar PostgreSQL para conexiones locales
sudo nano /etc/postgresql/12/main/pg_hba.conf
# Cambiar 'peer' por 'md5' para conexiones locales

sudo systemctl restart postgresql
```

### 3. Configurar Redis

```bash
# Configurar Redis
sudo nano /etc/redis/redis.conf
# Descomentar y configurar:
# bind 127.0.0.1
# requirepass tu_password_redis_seguro

sudo systemctl restart redis-server
sudo systemctl enable redis-server
```

### 4. Desplegar la Aplicación

```bash
# Crear usuario para la aplicación
sudo adduser rpgestor
sudo usermod -aG sudo rpgestor
su - rpgestor

# Clonar repositorio
git clone <repository-url> /home/rpgestor/rpgestor
cd /home/rpgestor/rpgestor

# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 5. Configurar Variables de Entorno

```bash
# Crear archivo de configuración
nano /home/rpgestor/rpgestor/.env
```

```env
# Configuración de producción
DEBUG=False
SECRET_KEY=clave_super_secreta_para_produccion_muy_larga_y_segura
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,IP_DEL_SERVIDOR

# Base de datos
DATABASE_URL=postgresql://rpgestor_user:password_super_seguro@localhost:5432/rpgestor_prod

# Redis
REDIS_URL=redis://:tu_password_redis_seguro@localhost:6379/0

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_password_de_aplicacion
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=RPGestor <noreply@tu-dominio.com>

# Archivos estáticos
STATIC_ROOT=/home/rpgestor/rpgestor/staticfiles
MEDIA_ROOT=/home/rpgestor/rpgestor/media
```

### 6. Configurar Django

```bash
# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Verificar configuración
python manage.py check --deploy
```

### 7. Configurar Gunicorn

```bash
# Crear archivo de configuración de Gunicorn
nano /home/rpgestor/rpgestor/gunicorn.conf.py
```

```python
# gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
daemon = False
user = "rpgestor"
group = "rpgestor"
tmp_upload_dir = None
errorlog = "/home/rpgestor/rpgestor/logs/gunicorn_error.log"
accesslog = "/home/rpgestor/rpgestor/logs/gunicorn_access.log"
loglevel = "info"
```

```bash
# Crear directorio de logs
mkdir -p /home/rpgestor/rpgestor/logs

# Probar Gunicorn
gunicorn rpgestor20.wsgi:application -c gunicorn.conf.py
```

### 8. Configurar Systemd

```bash
# Crear servicio systemd
sudo nano /etc/systemd/system/rpgestor.service
```

```ini
[Unit]
Description=RPGestor Django Application
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=rpgestor
Group=rpgestor
WorkingDirectory=/home/rpgestor/rpgestor
Environment=PATH=/home/rpgestor/rpgestor/venv/bin
ExecStart=/home/rpgestor/rpgestor/venv/bin/gunicorn rpgestor20.wsgi:application -c gunicorn.conf.py
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar y iniciar servicio
sudo systemctl daemon-reload
sudo systemctl enable rpgestor
sudo systemctl start rpgestor
sudo systemctl status rpgestor
```

### 9. Configurar Nginx

```bash
# Crear configuración de Nginx
sudo nano /etc/nginx/sites-available/rpgestor
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    client_max_body_size 100M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/rpgestor/rpgestor;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        root /home/rpgestor/rpgestor;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support
    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/rpgestor /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 10. Configurar SSL con Let's Encrypt

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Verificar renovación automática
sudo certbot renew --dry-run
```

## ☁️ Despliegue en Heroku

### 1. Preparar Archivos

```bash
# Crear Procfile
echo "web: gunicorn rpgestor20.wsgi:application" > Procfile
echo "worker: python manage.py runworker" >> Procfile

# Crear runtime.txt
echo "python-3.11.0" > runtime.txt

# Actualizar settings para Heroku
```

### 2. Configurar Heroku

```bash
# Instalar Heroku CLI
# Crear aplicación
heroku create tu-app-rpgestor

# Configurar variables de entorno
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=tu_clave_secreta
heroku config:set ALLOWED_HOSTS=tu-app-rpgestor.herokuapp.com

# Agregar add-ons
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev

# Desplegar
git push heroku main

# Ejecutar migraciones
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## 🐳 Despliegue con Docker

### 1. Crear Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "rpgestor20.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### 2. Crear docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: rpgestor_db
      POSTGRES_USER: rpgestor_user
      POSTGRES_PASSWORD: password123
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    command: redis-server --requirepass password123

  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://rpgestor_user:password123@db:5432/rpgestor_db
      - REDIS_URL=redis://:password123@redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./media:/app/media
      - ./staticfiles:/app/staticfiles

volumes:
  postgres_data:
```

### 3. Desplegar

```bash
# Construir y ejecutar
docker-compose up -d

# Ejecutar migraciones
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## 🔧 Configuración de Producción

### Settings de Producción

```python
# settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

# Seguridad
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/rpgestor/rpgestor/logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 📊 Monitoreo y Mantenimiento

### 1. Logs

```bash
# Ver logs de la aplicación
sudo journalctl -u rpgestor -f

# Ver logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Ver logs de PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-12-main.log
```

### 2. Backup

```bash
# Script de backup
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U rpgestor_user -h localhost rpgestor_prod > /backups/rpgestor_$DATE.sql
tar -czf /backups/media_$DATE.tar.gz /home/rpgestor/rpgestor/media/
```

### 3. Actualizaciones

```bash
# Actualizar código
cd /home/rpgestor/rpgestor
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart rpgestor
```

## 🚨 Solución de Problemas

### Error 502 Bad Gateway
```bash
# Verificar que Gunicorn esté ejecutándose
sudo systemctl status rpgestor

# Verificar logs
sudo journalctl -u rpgestor -n 50
```

### Error de Base de Datos
```bash
# Verificar conexión a PostgreSQL
sudo -u postgres psql -c "SELECT version();"

# Verificar configuración
python manage.py dbshell
```

### Error de Permisos
```bash
# Ajustar permisos
sudo chown -R rpgestor:rpgestor /home/rpgestor/rpgestor
sudo chmod -R 755 /home/rpgestor/rpgestor
```

¡Tu aplicación RPGestor está lista para producción! 🎉