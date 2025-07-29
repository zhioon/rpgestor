# 🚀 Guía de Despliegue en Railway - RPGestor

Esta guía te llevará paso a paso para desplegar tu aplicación RPGestor en Railway de forma **GRATUITA**.

## 🎯 ¿Por qué Railway?

- ✅ **$5 USD gratis** cada mes (suficiente para desarrollo)
- ✅ **PostgreSQL y Redis** incluidos gratis
- ✅ **Deploy automático** desde GitHub
- ✅ **SSL gratuito** y dominio personalizado
- ✅ **Muy fácil de configurar**
- ✅ **No se "duerme"** como Heroku

## 📋 Prerrequisitos

1. **Cuenta de GitHub** con tu proyecto RPGestor
2. **Cuenta de Railway** (gratis en https://railway.app)
3. **Tu proyecto** debe estar en GitHub

## 🚀 Paso a Paso - Despliegue Completo

### **1. Preparar tu Repositorio en GitHub**

```bash
# Si no tienes Git inicializado
git init
git add .
git commit -m "RPGestor v2.0 - Listo para producción"

# Crear repositorio en GitHub y subir
git remote add origin https://github.com/tu-usuario/rpgestor.git
git branch -M main
git push -u origin main
```

### **2. Crear Cuenta en Railway**

1. Ve a https://railway.app
2. Haz clic en **"Start a New Project"**
3. Conecta con tu cuenta de **GitHub**
4. Autoriza a Railway para acceder a tus repositorios

### **3. Crear Proyecto desde GitHub**

1. En Railway, haz clic en **"Deploy from GitHub repo"**
2. Selecciona tu repositorio **rpgestor**
3. Railway detectará automáticamente que es un proyecto Django
4. Haz clic en **"Deploy Now"**

### **4. Agregar Base de Datos PostgreSQL**

1. En tu proyecto de Railway, haz clic en **"+ New"**
2. Selecciona **"Database"**
3. Elige **"Add PostgreSQL"**
4. Railway creará automáticamente la base de datos
5. La variable `DATABASE_URL` se configurará automáticamente

### **5. Agregar Redis (Opcional pero Recomendado)**

1. Haz clic en **"+ New"** nuevamente
2. Selecciona **"Database"**
3. Elige **"Add Redis"**
4. La variable `REDIS_URL` se configurará automáticamente

### **6. Configurar Variables de Entorno**

En tu servicio web de Railway, ve a **"Variables"** y agrega:

```env
DEBUG=False
SECRET_KEY=tu-clave-super-secreta-cambiar-por-una-real
DJANGO_SETTINGS_MODULE=rpgestor20.settings_production
ALLOWED_HOSTS=.railway.app,.up.railway.app
```

**⚠️ IMPORTANTE**: Cambia `SECRET_KEY` por una clave real y segura.

### **7. Configurar Dominio Personalizado (Opcional)**

1. En tu servicio web, ve a **"Settings"**
2. En **"Domains"**, haz clic en **"Generate Domain"**
3. Railway te dará una URL como: `https://rpgestor-production.up.railway.app`

### **8. Verificar el Despliegue**

1. Ve a la pestaña **"Deployments"**
2. Verás el progreso del despliegue en tiempo real
3. Si hay errores, aparecerán en los logs

### **9. Ejecutar Migraciones y Crear Superusuario**

Una vez desplegado exitosamente:

1. Ve a tu servicio web en Railway
2. Haz clic en **"Connect"** para abrir la terminal
3. Ejecuta los siguientes comandos:

```bash
# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recopilar archivos estáticos (si es necesario)
python manage.py collectstatic --noinput
```

## 🎉 ¡Listo! Tu Aplicación Está Online

Tu aplicación estará disponible en la URL que Railway te proporcionó, por ejemplo:
**https://rpgestor-production.up.railway.app**

## 🔧 Configuración Avanzada

### **Variables de Entorno Completas**

```env
# Django
DEBUG=False
SECRET_KEY=tu-clave-super-secreta-de-50-caracteres-minimo
DJANGO_SETTINGS_MODULE=rpgestor20.settings_production

# Hosts permitidos
ALLOWED_HOSTS=.railway.app,.up.railway.app,tu-dominio-personalizado.com

# Base de datos (automático)
DATABASE_URL=postgresql://usuario:password@host:puerto/database

# Redis (automático)
REDIS_URL=redis://usuario:password@host:puerto

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-de-aplicacion
```

### **Generar SECRET_KEY Segura**

```python
# Ejecuta esto en Python para generar una clave segura
import secrets
print(secrets.token_urlsafe(50))
```

## 📊 Monitoreo y Logs

### **Ver Logs en Tiempo Real**
1. En Railway, ve a tu servicio web
2. Haz clic en **"View Logs"**
3. Verás todos los logs de tu aplicación

### **Métricas de Uso**
1. Ve a **"Metrics"** en tu proyecto
2. Verás CPU, memoria y tráfico de red
3. Monitorea que no excedas los $5 USD gratuitos

## 🔄 Actualizaciones Automáticas

Cada vez que hagas `git push` a tu repositorio:
1. Railway detectará los cambios automáticamente
2. Iniciará un nuevo despliegue
3. Tu aplicación se actualizará sin tiempo de inactividad

## 🛠️ Solución de Problemas

### **Error: "Application failed to respond"**
```bash
# Verificar que Gunicorn esté configurado correctamente
# En railway.json debe estar:
"startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn rpgestor20.wsgi:application --bind 0.0.0.0:$PORT"
```

### **Error: "ModuleNotFoundError"**
```bash
# Verificar que requirements.txt esté actualizado
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Actualizar requirements.txt"
git push
```

### **Error de Base de Datos**
```bash
# En la terminal de Railway:
python manage.py migrate --run-syncdb
```

### **Error de Archivos Estáticos**
```bash
# En la terminal de Railway:
python manage.py collectstatic --noinput --clear
```

## 💰 Costos y Límites

### **Plan Gratuito de Railway:**
- ✅ **$5 USD** de crédito mensual
- ✅ **PostgreSQL** incluido
- ✅ **Redis** incluido
- ✅ **SSL** gratuito
- ✅ **Dominio** personalizado

### **Uso Estimado para RPGestor:**
- **Aplicación web**: ~$2-3 USD/mes
- **PostgreSQL**: ~$1 USD/mes
- **Redis**: ~$0.50 USD/mes
- **Total**: ~$3.50-4.50 USD/mes (dentro del límite gratuito)

## 🎯 URLs de Acceso Final

Una vez desplegado, tendrás acceso a:

- **🌐 Aplicación Principal**: https://tu-app.up.railway.app
- **👤 Panel de Admin**: https://tu-app.up.railway.app/admin
- **📊 Dashboard**: https://tu-app.up.railway.app (según tu rol)
- **🔌 API**: https://tu-app.up.railway.app/api/v1/

## 📱 Compartir con tu Equipo

Puedes compartir la URL con:
- **👔 Gestores**: Para probar todas las funcionalidades
- **👨‍💼 Jefes de Ventas**: Para evaluar gestión de equipos
- **💼 Vendedores**: Para probar funcionalidades de campo
- **🎯 Stakeholders**: Para demostrar el sistema completo

## 🔒 Seguridad en Producción

### **Configuraciones Aplicadas Automáticamente:**
- ✅ **HTTPS** forzado
- ✅ **Headers de seguridad** configurados
- ✅ **DEBUG=False** en producción
- ✅ **Archivos estáticos** servidos eficientemente
- ✅ **Base de datos** con conexión segura

## 📈 Próximos Pasos

1. **🧪 Probar todas las funcionalidades** en producción
2. **👥 Crear usuarios de prueba** para demostración
3. **📊 Cargar datos de ejemplo** si es necesario
4. **📱 Planificar la app móvil** como siguiente fase
5. **🔄 Configurar backups** automáticos

## 🎉 ¡Felicitaciones!

Tu aplicación **RPGestor** está ahora **online y accesible desde cualquier lugar del mundo**. 

Puedes compartir la URL con tu equipo, clientes o stakeholders para que prueben el sistema completo.

**¡Tu proyecto está listo para impresionar! 🚀✨**

---

### 📞 Soporte

Si tienes problemas durante el despliegue:
1. Revisa los logs en Railway
2. Consulta la documentación en `docs/`
3. Verifica las variables de entorno
4. Asegúrate de que las migraciones se ejecutaron correctamente

¡Tu sistema de gestión de ventas está ahora disponible 24/7 en la nube! 🌐