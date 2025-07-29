from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from productos.models import Producto
from clientes.models import Cliente

@login_required
def calculadora_precios(request):
    """Vista para la calculadora de precios del vendedor"""
    
    # Obtener algunos productos para el dropdown
    productos = Producto.objects.all()[:100]  # Limitar para performance
    clientes = Cliente.objects.all()[:50]  # Algunos clientes para ejemplos
    
    context = {
        'productos': productos,
        'clientes': clientes,
    }
    
    return render(request, 'usuarios/calculadora_precios.html', context)

@csrf_exempt
@login_required
def ajax_calcular_precio(request):
    """AJAX endpoint para calcular precios en tiempo real"""
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Obtener datos del request
        producto_id = data.get('producto_id')
        cantidad = int(data.get('cantidad', 1))
        descuento_porcentaje = float(data.get('descuento', 0))
        tipo_precio = data.get('tipo_precio', 'precio1')  # precio1, precio2, precio3
        incluir_iva = data.get('incluir_iva', True)
        
        # Obtener producto
        producto = Producto.objects.get(pk=producto_id)
        
        # Obtener precio base según el tipo
        if tipo_precio == 'precio1':
            precio_base = float(producto.precio1)
        elif tipo_precio == 'precio2':
            precio_base = float(producto.precio2)
        elif tipo_precio == 'precio3':
            precio_base = float(producto.precio3)
        else:
            precio_base = float(producto.precio1)
        
        # Calcular descuento
        descuento_valor = precio_base * (descuento_porcentaje / 100)
        precio_con_descuento = precio_base - descuento_valor
        
        # Calcular subtotal
        subtotal = precio_con_descuento * cantidad
        
        # Calcular IVA
        iva_porcentaje = float(producto.iva)
        iva_valor = subtotal * (iva_porcentaje / 100) if incluir_iva else 0
        
        # Total final
        total = subtotal + iva_valor
        
        # Preparar respuesta
        resultado = {
            'success': True,
            'producto': {
                'codigo': producto.codigo,
                'nombre': producto.nombre,
                'stock': producto.stock,
            },
            'precios': {
                'precio_base': precio_base,
                'descuento_porcentaje': descuento_porcentaje,
                'descuento_valor': descuento_valor,
                'precio_con_descuento': precio_con_descuento,
                'cantidad': cantidad,
                'subtotal': subtotal,
                'iva_porcentaje': iva_porcentaje,
                'iva_valor': iva_valor,
                'total': total,
            },
            'formateo': {
                'precio_base': f"${precio_base:,.0f}",
                'descuento_valor': f"${descuento_valor:,.0f}",
                'precio_con_descuento': f"${precio_con_descuento:,.0f}",
                'subtotal': f"${subtotal:,.0f}",
                'iva_valor': f"${iva_valor:,.0f}",
                'total': f"${total:,.0f}",
            }
        }
        
        return JsonResponse(resultado)
        
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    except ValueError as e:
        return JsonResponse({'error': f'Error en los datos: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)