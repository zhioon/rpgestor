"""
Vistas específicas para el rol de Gestor
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q, Sum, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Vendedor
from pedidos.models import Pedido, ItemPedido
from productos.models import Producto, Grupo, SubGrupo
from clientes.models import Cliente
from django.contrib.auth.models import User

import logging
logger = logging.getLogger(__name__)

def es_gestor(user):
    return user.is_authenticated and user.groups.filter(name='Gestor').exists()

@user_passes_test(es_gestor, login_url='login')
def todos_los_pedidos(request):
    """Vista para mostrar todos los pedidos con filtros avanzados"""
    logger.info(f"Acceso a todos los pedidos por gestor: {request.user.username}")
    
    # Obtener todos los pedidos inicialmente
    pedidos = Pedido.objects.select_related(
        'cliente', 'vendedor__user'
    ).order_by('-created_at')
    
    # Obtener parámetros de filtro
    filtro_vendedor = request.GET.get('vendedor', '')
    filtro_grupo = request.GET.get('grupo', '')
    filtro_estado = request.GET.get('estado', '')
    filtro_fecha_inicio = request.GET.get('fecha_inicio', '')
    filtro_fecha_fin = request.GET.get('fecha_fin', '')
    filtro_cliente = request.GET.get('cliente', '')
    
    # Aplicar filtros
    if filtro_vendedor:
        pedidos = pedidos.filter(vendedor__id=filtro_vendedor)
    
    if filtro_estado:
        pedidos = pedidos.filter(estado=filtro_estado)
    
    if filtro_fecha_inicio:
        try:
            fecha_inicio = datetime.strptime(filtro_fecha_inicio, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha__gte=fecha_inicio)
        except ValueError:
            pass
    
    if filtro_fecha_fin:
        try:
            fecha_fin = datetime.strptime(filtro_fecha_fin, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha__lte=fecha_fin)
        except ValueError:
            pass
    
    if filtro_cliente:
        pedidos = pedidos.filter(
            Q(cliente__data__Empresa__icontains=filtro_cliente) |
            Q(cliente__data__Razon_Comercial__icontains=filtro_cliente) |
            Q(cliente__data__Nit__icontains=filtro_cliente)
        )
    
    # Filtro por grupo de productos
    if filtro_grupo:
        pedidos_con_grupo = ItemPedido.objects.filter(
            producto__grupo__id=filtro_grupo
        ).values_list('pedido__id', flat=True).distinct()
        pedidos = pedidos.filter(id__in=pedidos_con_grupo)
    
    # Estadísticas de los pedidos filtrados
    total_pedidos = pedidos.count()
    total_ventas = pedidos.aggregate(total=Sum('total'))['total'] or 0
    
    # Paginación
    paginator = Paginator(pedidos, 20)  # 20 pedidos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Datos para los filtros
    vendedores = Vendedor.objects.select_related('user').all()
    grupos = Grupo.objects.all()
    estados = Pedido.Estado.choices
    
    context = {
        'page_obj': page_obj,
        'total_pedidos': total_pedidos,
        'total_ventas': total_ventas,
        'vendedores': vendedores,
        'grupos': grupos,
        'estados': estados,
        'filtros': {
            'vendedor': filtro_vendedor,
            'grupo': filtro_grupo,
            'estado': filtro_estado,
            'fecha_inicio': filtro_fecha_inicio,
            'fecha_fin': filtro_fecha_fin,
            'cliente': filtro_cliente,
        }
    }
    
    return render(request, 'usuarios/gestor/todos_los_pedidos.html', context)

@user_passes_test(es_gestor, login_url='login')
def actualizar_bd_clientes(request):
    """Vista para actualizar la base de datos de clientes"""
    logger.info(f"Acceso a actualizar BD clientes por gestor: {request.user.username}")
    
    if request.method == 'POST':
        try:
            archivo = request.FILES.get('archivo_clientes')
            if not archivo:
                return JsonResponse({
                    'success': False,
                    'error': 'No se seleccionó ningún archivo'
                })
            
            # Validar tipo de archivo
            if not archivo.name.endswith(('.xlsx', '.csv')):
                return JsonResponse({
                    'success': False,
                    'error': 'Formato de archivo no válido. Use Excel (.xlsx) o CSV (.csv)'
                })
            
            # Procesar archivo
            import pandas as pd
            import io
            
            # Leer archivo según su tipo
            if archivo.name.endswith('.xlsx'):
                df = pd.read_excel(io.BytesIO(archivo.read()))
            else:
                df = pd.read_csv(io.BytesIO(archivo.read()))
            
            # Validar columnas requeridas
            columnas_requeridas = ['Codigo', 'Nit', 'Empresa', 'Email']
            columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
            
            if columnas_faltantes:
                return JsonResponse({
                    'success': False,
                    'error': f'Columnas faltantes: {", ".join(columnas_faltantes)}'
                })
            
            # Obtener opciones de procesamiento
            modo_actualizacion = request.POST.get('modo_actualizacion', 'actualizar')
            validar_email = request.POST.get('validar_email') == 'on'
            validar_nit = request.POST.get('validar_nit') == 'on'
            
            # Contadores para estadísticas
            clientes_creados = 0
            clientes_actualizados = 0
            errores = []
            
            # Procesar cada fila
            for index, row in df.iterrows():
                try:
                    # Validaciones básicas
                    if pd.isna(row['Codigo']) or pd.isna(row['Nit']):
                        errores.append(f"Fila {index + 2}: Código o NIT vacío")
                        continue
                    
                    # Validar email si está habilitado
                    if validar_email and not pd.isna(row['Email']):
                        import re
                        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                        if not re.match(email_pattern, str(row['Email'])):
                            errores.append(f"Fila {index + 2}: Email inválido")
                            continue
                    
                    # Preparar datos del cliente
                    datos_cliente = {
                        'Codigo': str(row['Codigo']),
                        'Nit': str(row['Nit']),
                        'Empresa': str(row['Empresa']) if not pd.isna(row['Empresa']) else '',
                        'Email': str(row['Email']) if not pd.isna(row['Email']) else '',
                        'Razon_Comercial': str(row.get('Razon_Comercial', '')) if not pd.isna(row.get('Razon_Comercial')) else '',
                        'Direccion': str(row.get('Direccion', '')) if not pd.isna(row.get('Direccion')) else '',
                        'Telefono': str(row.get('Telefono', '')) if not pd.isna(row.get('Telefono')) else '',
                        'Ciudad': str(row.get('Ciudad', '')) if not pd.isna(row.get('Ciudad')) else '',
                    }
                    
                    # Buscar cliente existente
                    cliente_existente = Cliente.objects.filter(
                        Q(data__Codigo=datos_cliente['Codigo']) | 
                        Q(data__Nit=datos_cliente['Nit'])
                    ).first()
                    
                    if cliente_existente:
                        if modo_actualizacion in ['actualizar', 'solo_actualizar']:
                            # Actualizar cliente existente
                            cliente_existente.data.update(datos_cliente)
                            cliente_existente.save()
                            clientes_actualizados += 1
                    else:
                        if modo_actualizacion in ['actualizar', 'solo_nuevos']:
                            # Crear nuevo cliente
                            Cliente.objects.create(data=datos_cliente)
                            clientes_creados += 1
                
                except Exception as e:
                    errores.append(f"Fila {index + 2}: {str(e)}")
            
            # Preparar respuesta
            resultado = {
                'success': True,
                'clientes_creados': clientes_creados,
                'clientes_actualizados': clientes_actualizados,
                'total_procesados': clientes_creados + clientes_actualizados,
                'errores': errores[:10],  # Mostrar solo los primeros 10 errores
                'total_errores': len(errores)
            }
            
            # Generar HTML de resultados
            html_resultados = f"""
            <div class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="bg-green-50 p-4 rounded-lg">
                        <div class="flex items-center">
                            <i class="fas fa-plus-circle text-green-600 text-xl mr-3"></i>
                            <div>
                                <p class="text-sm text-green-600">Clientes Creados</p>
                                <p class="text-2xl font-bold text-green-900">{clientes_creados}</p>
                            </div>
                        </div>
                    </div>
                    <div class="bg-blue-50 p-4 rounded-lg">
                        <div class="flex items-center">
                            <i class="fas fa-edit text-blue-600 text-xl mr-3"></i>
                            <div>
                                <p class="text-sm text-blue-600">Clientes Actualizados</p>
                                <p class="text-2xl font-bold text-blue-900">{clientes_actualizados}</p>
                            </div>
                        </div>
                    </div>
                    <div class="bg-red-50 p-4 rounded-lg">
                        <div class="flex items-center">
                            <i class="fas fa-exclamation-triangle text-red-600 text-xl mr-3"></i>
                            <div>
                                <p class="text-sm text-red-600">Errores</p>
                                <p class="text-2xl font-bold text-red-900">{len(errores)}</p>
                            </div>
                        </div>
                    </div>
                </div>
            """
            
            if errores:
                html_resultados += """
                <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                    <h4 class="font-medium text-yellow-900 mb-2">Errores Encontrados:</h4>
                    <ul class="text-sm text-yellow-800 space-y-1">
                """
                for error in errores[:10]:
                    html_resultados += f"<li>• {error}</li>"
                
                if len(errores) > 10:
                    html_resultados += f"<li>• ... y {len(errores) - 10} errores más</li>"
                
                html_resultados += "</ul></div>"
            
            html_resultados += "</div>"
            
            resultado['html'] = html_resultados
            
            return JsonResponse(resultado)
            
        except Exception as e:
            logger.error(f"Error al procesar archivo de clientes: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': f'Error al procesar el archivo: {str(e)}'
            })
    
    # Estadísticas actuales de clientes
    total_clientes = Cliente.objects.count()
    clientes_activos = Cliente.objects.filter(
        pedido__fecha__gte=timezone.now().date() - timedelta(days=30)
    ).distinct().count()
    
    context = {
        'total_clientes': total_clientes,
        'clientes_activos': clientes_activos,
    }
    
    return render(request, 'usuarios/gestor/actualizar_bd_clientes.html', context)

@user_passes_test(es_gestor, login_url='login')
def inventario_general(request):
    """Vista para mostrar el inventario general por grupos y subgrupos"""
    logger.info(f"Acceso a inventario general por gestor: {request.user.username}")
    
    # Obtener grupos con sus subgrupos y productos
    grupos = Grupo.objects.prefetch_related(
        'subgrupo_set__producto_set'
    ).all()
    
    # Estadísticas generales
    total_productos = Producto.objects.count()
    productos_sin_stock = Producto.objects.filter(stock=0).count()
    productos_stock_bajo = Producto.objects.filter(stock__lte=10, stock__gt=0).count()
    
    context = {
        'grupos': grupos,
        'total_productos': total_productos,
        'productos_sin_stock': productos_sin_stock,
        'productos_stock_bajo': productos_stock_bajo,
    }
    
    return render(request, 'usuarios/gestor/inventario_general.html', context)

@user_passes_test(es_gestor, login_url='login')
def subir_bd_productos(request):
    """Vista para subir base de datos de productos"""
    logger.info(f"Acceso a subir BD productos por gestor: {request.user.username}")
    
    if request.method == 'POST':
        # Aquí implementaremos la lógica de carga de archivos
        pass
    
    # Obtener grupos y subgrupos para el formulario
    grupos = Grupo.objects.prefetch_related('subgrupo_set').all()
    
    context = {
        'grupos': grupos,
    }
    
    return render(request, 'usuarios/gestor/subir_bd_productos.html', context)