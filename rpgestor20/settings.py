from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-d$a92%48knyiyd0)+=b$_0(s1sn7aq37nskdv04q8wp9=0hoi*'

DEBUG = True

# Permitir conexiones desde red local para desarrollo
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '192.168.*',  # Red local típica
    '10.*',       # Otra red local común
    '172.*',      # Otra red local común
]

# En desarrollo, permitir cualquier host
if DEBUG:
    ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Channels debe cargar antes que staticfiles
    'channels',

    # Static


    # Tus apps
    'notificaciones',
    'core.apps.CoreConfig',
    'productos.apps.ProductosConfig',
    'clientes.apps.ClientesConfig',
    'usuarios.apps.UsuariosConfig',
    'pedidos.apps.PedidosConfig',
    'insights.apps.InsightsConfig',
    'django.contrib.humanize',
    'mathfilters',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rpgestor20.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rpgestor20.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'es-co'

# Zona horaria de Colombia
TIME_ZONE = 'America/Bogota'

USE_I18N = True
USE_L10N = True
USE_TZ   = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuración de archivos de medios (fotos de perfil, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de autenticación
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'usuarios:dashboard_redirect'  # Redirige a la vista que determina el dashboard apropiado
LOGOUT_REDIRECT_URL = 'login'
# settings.py

# =============================================================================
# CONFIGURACIÓN DE EMAIL PARA PRODUCCIÓN
# =============================================================================

# OPCIÓN 1: GMAIL (Recomendado para empezar)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'rpgestordistrimayor@gmail.com'  # ← CAMBIAR POR TU EMAIL REAL
EMAIL_HOST_PASSWORD = 'wvoi rxua xkir iwjc'  # ← CAMBIAR POR TU APP PASSWORD REAL (16 caracteres)
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'RPGestor <rpgestordistrimayor@gmail.com>'  # ← Email con formato correcto


GESTOR_EMAIL = 'bucbeack8585@gmail.com'

CHANNEL_LAYERS = {
  'default': {
    'BACKEND': 'channels_redis.core.RedisChannelLayer',
    'CONFIG': { 'hosts': [('127.0.0.1', 6379)] },
  }
}

ASGI_APPLICATION = 'rpgestor20.asgi.application'

DATE_FORMAT      = 'd/m/Y'        # 22/07/2025
DATETIME_FORMAT  = 'd/m/Y H:i'    # 22/07/2025 14:30
SHORT_DATE_FORMAT = 'd/m/Y'
TIME_FORMAT      = 'H:i'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'usuarios': {  # Nombre de tu aplicación
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    }
}
