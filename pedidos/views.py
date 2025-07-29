import json
import csv
from django.shortcuts           import render, get_object_or_404
from django.http                import JsonResponse, HttpResponse
from django.urls                import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models           import Q

from clientes.models import Cliente
from usuarios.models import Vendedor
from productos.models import Producto
from .models import Pedido, ItemPedido

import csv
from io import StringIO
from django.shortcuts        import render, get_object_or_404, redirect
from django.http            import HttpResponse
from django.urls            import reverse
from django.core.mail       import EmailMessage
from django.conf            import settings
from django.contrib.auth.decorators import login_required

from .models import Pedido

def enviar_correo_gestor(pedido):
    """Envía automáticamente el correo al gestor con el pedido y CSV"""
    # 1) Generar CSV en memoria
    buf = StringIO()
    writer = csv.writer(buf, delimiter=';')
    for it in pedido.items.all():
        writer.writerow([
            it.producto.codigo,
            '',
            it.cantidad,
            f"{it.precio_unitario:.2f}"
        ])
    csv_bytes = buf.getvalue().encode('utf-8')

    # 2) Construir cuerpo del correo
    lineas = [
        f"PEDIDO FINALIZADO - #{pedido.pk}",
        f"Cliente: {pedido.cliente}",
        f"Vendedor: {pedido.vendedor.user.get_full_name() or pedido.vendedor.user.username}",
        f"Fecha: {pedido.fecha}",
        f"Estado: {pedido.get_estado_display()}",
        ""
    ]
    
    # Agregar nota si existe
    if pedido.nota:
        lineas.extend([
            "NOTA DEL PEDIDO:",
            f"{pedido.nota}",
            ""
        ])
    
    lineas.append("PRODUCTOS:")
    for it in pedido.items.all():
        subtotal = f"{it.subtotal:.2f}"
        lineas.append(f"  - {it.producto.codigo} | {it.producto.nombre} x {it.cantidad} = ${subtotal}")
    
    lineas.extend([
        "",
        f"Subtotal: ${pedido.total - pedido.iva_total:.2f}",
        f"IVA (19%): ${pedido.iva_total:.2f}",
        f"TOTAL: ${pedido.total:.2f}",
        "",
        "Este pedido ha sido finalizado automáticamente por el sistema.",
        "El archivo CSV con los detalles está adjunto."
    ])
    
    cuerpo = "\n".join(lineas)

    # 3) Enviar email
    gestor_email = getattr(settings, 'GESTOR_EMAIL', 'gestor@empresa.com')
    
    msg = EmailMessage(
        subject=f"[PEDIDO FINALIZADO] #{pedido.pk} - {pedido.cliente}",
        body=cuerpo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[gestor_email],
    )
    
    # Generar nombre de archivo más descriptivo
    nit_val = pedido.cliente.data.get('Nit', 'sin-nit')
    primer = pedido.items.first().producto if pedido.items.exists() else None
    if primer:
        subgrupo = primer.subgrupo.nombre
        grupo = primer.subgrupo.grupo.nombre
    else:
        grupo, subgrupo = 'sin-grupo', 'sin-subgrupo'
    
    safe = lambda x: str(x).replace(' ', '_')
    filename = f"PEDIDO_{pedido.pk}_{safe(grupo)}_{safe(subgrupo)}_{safe(nit_val)}.csv"
    
    msg.attach(filename, csv_bytes, 'text/csv')
    msg.send()

def enviar_correo_cliente(pedido, email_destino=None):
    """Envía correo al cliente con el resumen del pedido"""
    if email_destino:
        email_cliente = email_destino
    else:
        email_cliente = pedido.cliente.data.get('Email', '')
    
    if not email_cliente:
        raise ValueError("No se especificó email de destino para el cliente")
    
    # Construir cuerpo del correo para el cliente
    lineas = [
        f"Estimado cliente,",
        "",
        f"Su pedido #{pedido.pk} ha sido procesado exitosamente.",
        "",
        f"DETALLES DEL PEDIDO:",
        f"Empresa: {pedido.cliente.data.get('Empresa', 'N/A')}",
        f"NIT: {pedido.cliente.data.get('Nit', 'N/A')}",
        f"Fecha: {pedido.fecha}",
        f"Vendedor: {pedido.vendedor.user.get_full_name() or pedido.vendedor.user.username}",
        ""
    ]
    
    # Agregar nota si existe
    if pedido.nota:
        lineas.extend([
            "NOTA ESPECIAL:",
            f"{pedido.nota}",
            ""
        ])
    
    lineas.append("PRODUCTOS SOLICITADOS:")
    for it in pedido.items.all():
        lineas.append(f"  • {it.producto.nombre} (Código: {it.producto.codigo})")
        lineas.append(f"    Cantidad: {it.cantidad} unidades")
        lineas.append(f"    Precio unitario: ${it.precio_unitario:.2f}")
        lineas.append(f"    Subtotal: ${it.subtotal:.2f}")
        lineas.append("")
    
    lineas.extend([
        f"RESUMEN:",
        f"Subtotal: ${pedido.total - pedido.iva_total:.2f}",
        f"IVA (19%): ${pedido.iva_total:.2f}",
        f"TOTAL: ${pedido.total:.2f}",
        "",
        "Su pedido será procesado y despachado según nuestros tiempos habituales.",
        "Gracias por su confianza.",
        "",
        "Atentamente,",
        "Equipo de Ventas"
    ])
    
    cuerpo = "\n".join(lineas)
    
    msg = EmailMessage(
        subject=f"Confirmación de Pedido #{pedido.pk}",
        body=cuerpo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email_cliente],
    )
    msg.send()

@login_required
def crear_pedido(request):
    """Renderiza la página base; el flujo es todo AJAX/JS."""
    clientes = Cliente.objects.all()
    
    # Verificar si se pasó un cliente preseleccionado
    cliente_preseleccionado = None
    cliente_id = request.GET.get('cliente')
    if cliente_id:
        try:
            cliente_preseleccionado = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            cliente_preseleccionado = None
    
    return render(request, 'pedidos/crear_pedido.html', {
        'clientes': clientes,
        'cliente_preseleccionado': cliente_preseleccionado,
    })

@login_required
def ajax_buscar_cliente(request):
    q = request.GET.get('q', '').strip()
    lista = []
    
    print(f"🔍 Búsqueda: '{q}'")
    
    if q and len(q) >= 2:
        try:
            # Obtener todos los clientes y filtrar en Python
            todos_los_clientes = Cliente.objects.all()
            
            clientes_filtrados = []
            for c in todos_los_clientes:
                # Asegurarse de que 'data' no sea None y sea un diccionario
                if isinstance(c.data, dict):
                    # Convertir todos los valores a string para una búsqueda insensible a mayúsculas y minúsculas
                    nit = str(c.data.get('Nit', '')).lower()
                    empresa = str(c.data.get('Empresa', '')).lower()
                    razon = str(c.data.get('Razon_Comercial', '')).lower()
                    codigo = str(c.data.get('Codigo', '')).lower()
                    q_lower = q.lower()

                    if (q_lower in nit or 
                        q_lower in empresa or 
                        q_lower in razon or 
                        q_lower in codigo):
                        clientes_filtrados.append(c)

            print(f"🎯 Encontrados: {len(clientes_filtrados)}")

            for c in clientes_filtrados[:10]:  # Limitar a 10 resultados
                lista.append({
                    'id': c.pk,
                    'nit': str(c.data.get('Nit', '')),
                    'empresa': c.data.get('Empresa', ''),
                    'razon': c.data.get('Razon_Comercial', ''),
                    'direccion': c.data.get('Direccion', ''),
                    'codigo': str(c.data.get('Codigo', ''))
                })
                
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            
    print(f"📤 Enviando: {len(lista)} resultados")
    return JsonResponse({'clientes': lista})

@login_required
def ajax_price_types(request, cliente_id):
    tipos = [{'value': i, 'label': f'Precio {i}'} for i in range(1,7)]
    return JsonResponse({'price_types': tipos})

@login_required
def ajax_productos(request, cliente_id, price_type):
    vendedor = Vendedor.objects.get(user=request.user)
    campo_precio = f'precio{price_type}'
    productos = Producto.objects.filter(
        subgrupo__in=vendedor.subgrupos.all()
    )
    data = []
    for p in productos:
        precio = float(getattr(p, campo_precio))
        if float(p.iva):
            precio *= 1 + float(p.iva)/100
        data.append({
            'id':         p.pk,
            'codigo':     p.codigo,
            'nombre':     p.nombre,
            'precio':     round(precio,2),
            'stock':      p.stock,
            'descuento':  float(p.descuento),
            'tiene_promocion': bool(float(p.descuento)),
            'imagen_url': p.imagen.url if p.imagen else '', 
        })
    return JsonResponse({'productos': data})

@csrf_exempt
@login_required
def confirmar_pedido(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        print(f"Datos recibidos: {data}")  # Debug log
        
        cliente = get_object_or_404(Cliente, pk=data['cliente'])
        vendedor = Vendedor.objects.get(user=request.user)
        
        pedido = Pedido.objects.create(
            cliente=cliente,
            vendedor=vendedor,
            estado=Pedido.Estado.ENVIADO,
            nota=data.get('nota', '')
        )
        
        total, total_iva = 0, 0

        for it in data['items']:
            print(f"Procesando item: {it}")  # Debug log
            prod = get_object_or_404(Producto, pk=it['producto'])
            cantidad = int(it['cantidad'])
            
            # Crear item del pedido
            item = ItemPedido.objects.create(
                pedido=pedido,
                producto=prod,
                cantidad=cantidad,
                precio_unitario=prod.precio1,
                descuento=0
            )
            
            # Actualizar stock
            prod.stock -= cantidad
            prod.save()
            
            # Calcular totales
            total += item.subtotal
            total_iva += item.subtotal * (prod.iva/100)

        pedido.total = total + total_iva
        pedido.iva_total = total_iva
        pedido.save()

        redirect_url = reverse('pedidos:detalle_pedido', args=[pedido.pk])
        print(f"Pedido creado exitosamente: {pedido.pk}, redirigiendo a: {redirect_url}")  # Debug log
        
        return JsonResponse({
            'success': True,
            'pedido_id': pedido.pk,
            'redirect_url': redirect_url
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except KeyError as e:
        return JsonResponse({'error': f'Campo requerido faltante: {e}'}, status=400)
    except Vendedor.DoesNotExist:
        return JsonResponse({'error': 'Vendedor no encontrado'}, status=400)
    except Exception as e:
        print(f"Error al confirmar pedido: {e}")  # Debug log
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

@login_required
def detalle_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    return render(request, 'pedidos/detalle_pedido_nuevo.html', {
        'pedido': pedido
    })

@csrf_exempt
@login_required
def finalizar_pedido(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        pedido = get_object_or_404(Pedido, pk=pk)
        
        # Verificar que el pedido esté en estado ENVIADO
        if pedido.estado != Pedido.Estado.ENVIADO:
            return JsonResponse({'error': 'El pedido no está en estado válido para finalizar'}, status=400)
        
        data = json.loads(request.body)
        enviar_cliente = data.get('enviar_cliente', False)
        email_option = data.get('email_option', 'bd')
        email_cliente_manual = data.get('email_cliente', '')
        
        print(f"Finalizando pedido {pk}, enviar_cliente: {enviar_cliente}, email_option: {email_option}")
        
        # Cambiar estado a FINALIZADO
        pedido.estado = Pedido.Estado.FINALIZADO
        pedido.save()
        
        # Generar y enviar correo al gestor (automático)
        correo_gestor_enviado = False
        try:
            enviar_correo_gestor(pedido)
            correo_gestor_enviado = True
            print(f"Correo enviado al gestor para pedido {pk}")
        except Exception as e:
            print(f"Error al enviar correo al gestor: {e}")
            # No fallar si el correo al gestor falla, pero log el error
        
        # Enviar correo al cliente si se solicitó
        correo_cliente_enviado = False
        if enviar_cliente:
            try:
                # Determinar el email a usar
                if email_option == 'manual':
                    email_destino = email_cliente_manual
                else:
                    email_destino = pedido.cliente.data.get('Email', '')
                
                if not email_destino:
                    raise ValueError("No se especificó email de destino")
                
                enviar_correo_cliente(pedido, email_destino)
                correo_cliente_enviado = True
                print(f"Correo enviado al cliente ({email_destino}) para pedido {pk}")
            except Exception as e:
                print(f"Error al enviar correo al cliente: {e}")
                # No fallar si el correo al cliente falla, pero incluir el error en la respuesta
                return JsonResponse({
                    'success': True,
                    'message': 'Pedido finalizado exitosamente, pero hubo un error al enviar el correo al cliente',
                    'pedido_id': pedido.pk,
                    'correo_gestor': correo_gestor_enviado,
                    'correo_cliente': False,
                    'error_cliente': str(e)
                })
        
        return JsonResponse({
            'success': True,
            'message': 'Pedido finalizado exitosamente',
            'pedido_id': pedido.pk,
            'correo_gestor': True,
            'correo_cliente': enviar_cliente
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        print(f"Error al finalizar pedido: {e}")
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

@login_required
def detalle_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    # intentamos extraer email del cliente
    email_cliente = pedido.cliente.data.get('Email', '')
    return render(request, 'pedidos/detalle_pedido.html', {
        'pedido':       pedido,
        'email_cliente': email_cliente,
    })

@login_required
def descargar_csv(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    # 1) Extracción de grupo, subgrupo y NIT
    nit_val = pedido.cliente.data.get('Nit', 'sin-nit')
    primer = pedido.items.first().producto if pedido.items.exists() else None
    if primer:
        subgrupo = primer.subgrupo.nombre
        grupo    = primer.subgrupo.grupo.nombre
    else:
        grupo, subgrupo = 'sin-grupo','sin-subgrupo'

    # 2) Sanitizar valores (convertir siempre a str)
    safe = lambda x: str(x).replace(' ', '_')
    filename = f"{safe(grupo)}-{safe(subgrupo)}-{safe(nit_val)}.csv"

    # 3) Generar CSV en memoria
    buf    = StringIO()
    writer = csv.writer(buf, delimiter=';')
    for item in pedido.items.all():
        writer.writerow([
            item.producto.codigo,
            '',
            item.cantidad,
            f"{item.precio_unitario:.2f}",
        ])

    # 4) Devolver como descarga
    resp = HttpResponse(buf.getvalue(), content_type='text/csv')
    resp['Content-Disposition'] = f'attachment; filename="{filename}"'
    return resp

@login_required
def enviar_pedido_gestor(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    # 1) Generar CSV en memoria
    buf = StringIO()
    writer = csv.writer(buf, delimiter=';')
    for it in pedido.items.all():
        writer.writerow([
            it.producto.codigo,
            '',
            it.cantidad,
            f"{it.precio_unitario:.2f}"
        ])
    csv_bytes = buf.getvalue().encode('utf-8')

    # 2) Construir cuerpo del correo
    lineas = [
        f"Pedido #{pedido.pk}",
        f"Cliente: {pedido.cliente}",
        f"Fecha:   {pedido.fecha}",
        "",
        "Items:"
    ]
    for it in pedido.items.all():
        subtotal = f"{it.subtotal:.2f}"
        lineas.append(f"  - {it.producto.codigo} | {it.producto.nombre} x {it.cantidad} = {subtotal}")
    lineas += [
        "",
        f"IVA Total: {pedido.iva_total:.2f}",
        f"Total:     {pedido.total:.2f}",
    ]
    cuerpo = "\n".join(lineas)

    # 3) Enviar email
    gestor_email = settings.GESTOR_EMAIL
    msg = EmailMessage(
        subject=f"[Gestor] Pedido #{pedido.pk}",
        body=cuerpo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[gestor_email],
    )
    msg.attach(f"pedido_{pedido.pk}.csv", csv_bytes, 'text/csv')
    msg.send()  # con ConsoleBackend, verás el contenido en la terminal

    # 4) Redirigir de nuevo al detalle
    return redirect('usuarios:dashboard_redirect')

@login_required
def enviar_pedido_cliente(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == 'POST':
        # Recogemos el email desde el formulario
        to_email = request.POST.get('email')
        # Generamos el CSV en memoria
        buf = StringIO()
        writer = csv.writer(buf, delimiter=';')
        for it in pedido.items.all():
            writer.writerow([it.producto.codigo, '', it.cantidad, f"{it.precio_unitario:.2f}"])
        csv_bytes = buf.getvalue().encode('utf-8')

        # Construimos el cuerpo del correo
        cuerpo = ["Pedido #%d para cliente" % pedido.pk,
                  f"Cliente: {pedido.cliente}",
                  f"Fecha:   {pedido.fecha}",
                  "", "Items:"]
        for it in pedido.items.all():
            cuerpo.append(f"- {it.producto.codigo} | {it.producto.nombre} x {it.cantidad} = {it.subtotal:.2f}")
        cuerpo.append(f"\nTotal: {pedido.total:.2f}")
        body = "\n".join(cuerpo)

        # Enviamos
        msg = EmailMessage(
            subject=f"Pedido #{pedido.pk}",
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        msg.attach(f"pedido_{pedido.pk}.csv", csv_bytes, 'text/csv')
        msg.send()
        return redirect('usuarios:dashboard_redirect')

    # GET: mostramos el formulario con el email por defecto del cliente
    email_cliente = pedido.cliente.data.get('Email', '')
    return render(request, 'pedidos/enviar_cliente.html', {
        'pedido': pedido,
        'email': email_cliente,
    })
@login_required
def mis_pedidos(request):
    """Vista para mostrar el historial de pedidos del vendedor actual"""
    # Obtener el objeto Vendedor del usuario actual
    try:
        vendedor = Vendedor.objects.get(user=request.user)
        # Obtener los pedidos del vendedor actual
        pedidos = Pedido.objects.filter(vendedor=vendedor).order_by('-created_at')
    except Vendedor.DoesNotExist:
        pedidos = Pedido.objects.none()
    
    return render(request, 'pedidos/mis_pedidos.html', {
        'pedidos': pedidos
    })

@login_required
def historial_cliente(request, cliente_id):
    """Vista para mostrar el historial de pedidos de un cliente específico"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    # Verificar que el vendedor tenga acceso a este cliente
    try:
        vendedor = Vendedor.objects.get(user=request.user)
        # Solo mostrar pedidos del vendedor actual para este cliente
        pedidos = Pedido.objects.filter(
            cliente=cliente,
            vendedor=vendedor
        ).order_by('-created_at')
    except Vendedor.DoesNotExist:
        pedidos = Pedido.objects.none()
    
    return render(request, 'pedidos/historial_cliente.html', {
        'cliente': cliente,
        'pedidos': pedidos
    })