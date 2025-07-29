"""
Vistas simplificadas para productos sin pandas
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count

from .forms import UploadExcelForm
from .models import Grupo, SubGrupo, Producto, StockMovimiento
from usuarios.models import Vendedor

def pandas_not_available_error(request, redirect_url='productos:inventario_gestor'):
    """Helper function para mostrar error cuando pandas no está disponible"""
    messages.error(request, "Función de importación temporalmente deshabilitada. Pandas no está instalado.")
    return redirect(redirect_url)

@login_required
def import_products(request):
    """Importa el Excel de productos + stock masivo - TEMPORALMENTE DESHABILITADO"""
    count = 0
    errors = []
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            # Función temporalmente deshabilitada - requiere pandas
            errors.append("Función de importación temporalmente deshabilitada. Contacte al administrador.")
            return render(request, 'productos/import.html', {
                'form': form,
                'count': count,
                'errors': errors,
            })
    else:
        form = UploadExcelForm()

    return render(request, 'productos/import.html', {
        'form': form,
        'count': count,
        'errors': errors,
    })

@login_required
def mis_productos(request):
    """Muestra los productos asignados al vendedor actual."""
    vendedor = get_object_or_404(Vendedor, user=request.user)
    productos = Producto.objects.filter(subgrupo__in=vendedor.subgrupos.all())
    return render(request, 'productos/mis_productos.html', {
        'productos': productos
    })

@login_required
def movimientos_stock(request, producto_id):
    """Historial de movimientos de stock para un producto dado."""
    producto = get_object_or_404(Producto, id=producto_id)
    movimientos = StockMovimiento.objects.filter(producto=producto).order_by('-fecha')
    
    paginator = Paginator(movimientos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'productos/movimientos_stock.html', {
        'producto': producto,
        'page_obj': page_obj,
    })

@login_required
def inventario_vendedor(request):
    """Muestra el inventario asignado al vendedor logueado."""
    vendedor = get_object_or_404(Vendedor, user=request.user)
    
    # Filtros
    grupo_id = request.GET.get('grupo')
    subgrupo_id = request.GET.get('subgrupo')
    busqueda = request.GET.get('busqueda', '')
    
    # Query base
    productos = Producto.objects.filter(subgrupo__in=vendedor.subgrupos.all())
    
    # Aplicar filtros
    if grupo_id:
        productos = productos.filter(subgrupo__grupo_id=grupo_id)
    if subgrupo_id:
        productos = productos.filter(subgrupo_id=subgrupo_id)
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) | 
            Q(codigo__icontains=busqueda)
        )
    
    # Paginación
    paginator = Paginator(productos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Datos para filtros
    grupos = Grupo.objects.filter(subgrupos__in=vendedor.subgrupos.all()).distinct()
    subgrupos = vendedor.subgrupos.all()
    
    return render(request, 'productos/inventario_vendedor.html', {
        'page_obj': page_obj,
        'grupos': grupos,
        'subgrupos': subgrupos,
        'grupo_seleccionado': grupo_id,
        'subgrupo_seleccionado': subgrupo_id,
        'busqueda': busqueda,
    })

def es_jefe_de_ventas(user):
    """Verifica si el usuario es jefe de ventas"""
    return user.groups.filter(name='JefeVentas').exists()

@user_passes_test(es_jefe_de_ventas)
def inventario_jefe(request):
    """Muestra inventario para jefe de ventas."""
    # Filtros
    grupo_id = request.GET.get('grupo')
    subgrupo_id = request.GET.get('subgrupo')
    vendedor_id = request.GET.get('vendedor')
    busqueda = request.GET.get('busqueda', '')
    
    # Query base
    productos = Producto.objects.all()
    
    # Aplicar filtros
    if grupo_id:
        productos = productos.filter(subgrupo__grupo_id=grupo_id)
    if subgrupo_id:
        productos = productos.filter(subgrupo_id=subgrupo_id)
    if vendedor_id:
        vendedor = get_object_or_404(Vendedor, id=vendedor_id)
        productos = productos.filter(subgrupo__in=vendedor.subgrupos.all())
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) | 
            Q(codigo__icontains=busqueda)
        )
    
    # Paginación
    paginator = Paginator(productos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Datos para filtros
    grupos = Grupo.objects.all()
    subgrupos = SubGrupo.objects.all()
    vendedores = Vendedor.objects.all()
    
    return render(request, 'productos/inventario_jefe.html', {
        'page_obj': page_obj,
        'grupos': grupos,
        'subgrupos': subgrupos,
        'vendedores': vendedores,
        'grupo_seleccionado': grupo_id,
        'subgrupo_seleccionado': subgrupo_id,
        'vendedor_seleccionado': vendedor_id,
        'busqueda': busqueda,
    })

def es_gestor(user):
    """Verifica si el usuario es gestor"""
    return user.is_authenticated and user.groups.filter(name='Gestor').exists()

@user_passes_test(es_gestor, login_url='login')
def inventario_gestor(request):
    """Vista del inventario general para gestores."""
    # Filtros
    grupo_id = request.GET.get('grupo')
    subgrupo_id = request.GET.get('subgrupo')
    busqueda = request.GET.get('busqueda', '')
    
    # Query base
    productos = Producto.objects.all()
    
    # Aplicar filtros
    if grupo_id:
        productos = productos.filter(subgrupo__grupo_id=grupo_id)
    if subgrupo_id:
        productos = productos.filter(subgrupo_id=subgrupo_id)
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) | 
            Q(codigo__icontains=busqueda)
        )
    
    # Estadísticas
    total_productos = productos.count()
    total_stock = productos.aggregate(total=Sum('stock'))['total'] or 0
    
    # Paginación
    paginator = Paginator(productos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Datos para filtros
    grupos = Grupo.objects.all()
    subgrupos = SubGrupo.objects.all()
    
    return render(request, 'productos/inventario_gestor.html', {
        'page_obj': page_obj,
        'grupos': grupos,
        'subgrupos': subgrupos,
        'grupo_seleccionado': grupo_id,
        'subgrupo_seleccionado': subgrupo_id,
        'busqueda': busqueda,
        'total_productos': total_productos,
        'total_stock': total_stock,
    })

@user_passes_test(es_gestor, login_url='login')
def subir_bd_productos_gestor(request):
    """Vista para subir BD de productos - TEMPORALMENTE DESHABILITADO"""
    messages.error(request, "Función de importación temporalmente deshabilitada. Pandas no está instalado.")
    return redirect('productos:inventario_gestor')

@user_passes_test(es_gestor, login_url='login')
def actualizar_bd_productos_gestor(request):
    """Vista para actualizar BD de productos - TEMPORALMENTE DESHABILITADO"""
    messages.error(request, "Función de importación temporalmente deshabilitada. Pandas no está instalado.")
    return redirect('productos:inventario_gestor')