import pandas as pd
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import UploadExcelForm
from .models import Cliente
from usuarios.models import Vendedor

def import_clients_full(request):
    count = 0
    errors = []
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            df = pd.read_excel(
                request.FILES['excel_file'],
                header=0,
                engine='openpyxl'
            ).fillna('')

            for idx, row in df.iterrows():
                try:
                    # Convertir cada valor al tipo JSON-serializable
                    raw = row.to_dict()
                    data = {}
                    for key, val in raw.items():
                        if isinstance(val, pd.Timestamp):
                            # convierte Timestamp a ISO string
                            data[key] = val.isoformat()
                        elif isinstance(val, (datetime.date, datetime.datetime)):
                            # otras fechas
                            data[key] = val.isoformat()
                        else:
                            data[key] = val

                    nit = data.get('Nit') or f"sin-nit-{idx}"
                    Cliente.objects.update_or_create(
                        defaults={'data': data},
                        data__Nit=nit
                    )
                    count += 1

                except Exception as e:
                    errors.append(f"Fila {idx+2}: {e}")
    else:
        form = UploadExcelForm()

    return render(request, 'clientes/import_full.html', {
        'form': form,
        'count': count,
        'errors': errors
    })

@login_required
def lista_clientes(request):
    """Vista para mostrar todos los clientes con búsqueda y paginación"""
    # Obtener parámetros de búsqueda
    search_query = request.GET.get('search', '').strip()
    
    # Obtener todos los clientes
    clientes = Cliente.objects.all().order_by('id')
    
    # Aplicar filtro de búsqueda si existe
    if search_query:
        clientes = clientes.filter(
            Q(data__Empresa__icontains=search_query) |
            Q(data__Razon_Comercial__icontains=search_query) |
            Q(data__Nit__icontains=search_query) |
            Q(data__Codigo__icontains=search_query) |
            Q(data__Direccion__icontains=search_query)
        )
    
    # Obtener el vendedor actual para verificar favoritos
    try:
        vendedor = Vendedor.objects.get(user=request.user)
        # Obtener IDs de clientes favoritos
        favoritos_ids = vendedor.clientes_favoritos.values_list('cliente_id', flat=True)
    except Vendedor.DoesNotExist:
        vendedor = None
        favoritos_ids = []
    
    # Paginación
    paginator = Paginator(clientes, 20)  # 20 clientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'clientes/lista_clientes.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_clientes': clientes.count(),
        'favoritos_ids': favoritos_ids,
        'vendedor': vendedor,
    })

@login_required
def clientes_favoritos(request):
    """Vista para mostrar solo los clientes favoritos del vendedor"""
    try:
        vendedor = Vendedor.objects.get(user=request.user)
        # Obtener clientes favoritos del vendedor
        favoritos = vendedor.clientes_favoritos.select_related('cliente').order_by('-created_at')
        
        # Extraer los clientes de los favoritos
        clientes_favoritos = [fav.cliente for fav in favoritos]
        
        # Aplicar búsqueda si existe
        search_query = request.GET.get('search', '').strip()
        if search_query:
            clientes_favoritos = [
                cliente for cliente in clientes_favoritos
                if (search_query.lower() in str(cliente.data.get('Empresa', '')).lower() or
                    search_query.lower() in str(cliente.data.get('Razon_Comercial', '')).lower() or
                    search_query.lower() in str(cliente.data.get('Nit', '')).lower() or
                    search_query.lower() in str(cliente.data.get('Codigo', '')).lower())
            ]
        
        # Paginación
        paginator = Paginator(clientes_favoritos, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
    except Vendedor.DoesNotExist:
        page_obj = None
        search_query = ''
        favoritos = []
    
    return render(request, 'clientes/clientes_favoritos.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_favoritos': len(clientes_favoritos) if 'clientes_favoritos' in locals() else 0,
    })

@login_required
def toggle_favorito(request, cliente_id):
    """Vista AJAX para agregar/quitar cliente de favoritos"""
    if request.method == 'POST':
        try:
            vendedor = Vendedor.objects.get(user=request.user)
            cliente = get_object_or_404(Cliente, id=cliente_id)
            
            # Verificar si ya es favorito
            from .models import ClienteFavorito
            favorito, created = ClienteFavorito.objects.get_or_create(
                vendedor=vendedor,
                cliente=cliente
            )
            
            if not created:
                # Si ya existía, lo eliminamos (toggle off)
                favorito.delete()
                is_favorito = False
                message = "Cliente eliminado de favoritos"
            else:
                # Si es nuevo, lo mantenemos (toggle on)
                is_favorito = True
                message = "Cliente agregado a favoritos"
            
            return JsonResponse({
                'success': True,
                'is_favorito': is_favorito,
                'message': message
            })
            
        except Vendedor.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Vendedor no encontrado'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
def detalle_cliente(request, cliente_id):
    """Vista para mostrar el detalle completo de un cliente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    # Verificar si es favorito del vendedor actual
    is_favorito = False
    try:
        vendedor = Vendedor.objects.get(user=request.user)
        from .models import ClienteFavorito
        is_favorito = ClienteFavorito.objects.filter(
            vendedor=vendedor,
            cliente=cliente
        ).exists()
    except Vendedor.DoesNotExist:
        pass
    
    # Obtener pedidos del cliente (opcional)
    from pedidos.models import Pedido
    pedidos_recientes = Pedido.objects.filter(cliente=cliente).order_by('-created_at')[:5]
    
    return render(request, 'clientes/detalle_cliente.html', {
        'cliente': cliente,
        'is_favorito': is_favorito,
        'pedidos_recientes': pedidos_recientes,
    })