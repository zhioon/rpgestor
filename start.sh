#!/bin/bash

# Script de inicio para Railway
echo "🚀 Iniciando RPGestor..."

# Ejecutar migraciones
echo "📊 Ejecutando migraciones..."
python manage.py migrate --noinput

# Recopilar archivos estáticos
echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar servidor
echo "🌐 Iniciando servidor Gunicorn..."
exec gunicorn rpgestor20.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120