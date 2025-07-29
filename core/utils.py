import csv
from django.http import HttpResponse

def format_price(value):
    """
    Recibe un número (int, float o str numérico) y devuelve
    una cadena con separadores de miles “.”, sin decimales.
    Ejemplo: 1234567 → "1.234.567"
    """
    try:
        # Convertir a entero y formatear
        return f"{int(value):,}".replace(",", ".")
    except (ValueError, TypeError):
        # Si no es convertible, devolver tal cual
        return value

def export_queryset_to_csv(queryset, fields, filename='export.csv'):
    """
    Toma un QuerySet, una lista de nombres de campos y devuelve
    un HttpResponse con un CSV listo para descargar.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    # Encabezados
    writer.writerow(fields)
    # Filas
    for obj in queryset:
        writer.writerow([getattr(obj, f) for f in fields])
    return response
