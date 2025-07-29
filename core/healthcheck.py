"""
Vista de healthcheck para Railway y otros servicios de hosting
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
@require_http_methods(["GET"])
def healthcheck(request):
    """
    Vista simple de healthcheck que responde con status 200
    para que Railway sepa que la aplicación está funcionando
    """
    return JsonResponse({
        'status': 'healthy',
        'message': 'RPGestor está funcionando correctamente',
        'version': '2.0.0'
    })

@csrf_exempt
@require_http_methods(["GET"])
def status(request):
    """
    Vista de status más detallada
    """
    try:
        # Verificar conexión a base de datos
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return JsonResponse({
        'status': 'ok',
        'database': db_status,
        'application': 'RPGestor',
        'version': '2.0.0'
    })