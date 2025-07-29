from django.shortcuts        import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms                  import UploadExcelForm
from .models                 import Grupo, SubGrupo, Producto, StockMovimiento
from usuarios.models         import Vendedor
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

def pandas_not_available_error(request, redirect_url='productos:inventario_gestor'):
    """Helper function para mostrar error cuando pandas no está disponible"""
    messages.error(request, "Función de importación temporalmente deshabilitada. Pandas no está instalado.")
    return redirect(redirect_url)

@login_required
def import_products(request):
    """
    Importa el Excel de productos + stock masivo.
    Para cada fila:
      1. Crea/actualiza Grupo y SubGrupo.
      2. Si el Producto ya existía, calcula la diferencia de stock.
         - Si la diferencia != 0, crea un StockMovimiento (ENT/SAL).
      3. Crea o actualiza el Producto con todos sus campos, incluyendo el stock nuevo.
    """
    count  = 0
    errors = []

    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            # Función de importación temporalmente deshabilitada - requiere pandas
            errors.append("Función de importación temporalmente deshabilitada. Contacte al administrador.")
            return render(request, 'productos/import.html', {
                'form': form,
                'count': count,
                'errors': errors,
            })
            
            # TODO: Implementar importación sin pandas o agregar pandas al requirements.txt
            """
            # Código original comentado hasta agregar pandas:
            df = pd.read_excel(
                request.FILES['excel_file'],
                header=4,
                engine='openpyxl'
            ).fillna(0)

            for idx, row in df.iterrows():
                try:
                    # 1) Grupo / SubGrupo
                    grupo, _ = Grupo.objects.get_or_create(nombre=row['Grupo'])
                    subg, _  = SubGrupo.objects.get_or_create(
                        nombre=row['Sub Grupo'],
                        grupo=grupo
                    )

                    # 2) Si existe, captura stock anterior
                    codigo = str(row['codigo']).strip()
                    try:
                        prod = Producto.objects.get(codigo=codigo)
                        anterior_stock = prod.stock or 0
                        nuevo_stock    = int(row['stock'])
                        diferencia     = nuevo_stock - anterior_stock
                    except Producto.DoesNotExist:
                        prod = None
                        anterior_stock = 0
                        nuevo_stock    = int(row['stock'])
                        diferencia     = nuevo_stock

                    # 3) Crear movimiento si hay diferencia
                    if diferencia != 0:
                        StockMovimiento.objects.create(
                            producto    = prod if prod else Producto(codigo=codigo),
                            tipo        = 'ENT' if diferencia > 0 else 'SAL',
                            cantidad    = abs(diferencia),
                            responsable = request.user,
                            notas       = 'Importación masiva de stock'
                        )

                    # 4) Crear o actualizar Producto
                    prod, _ = Producto.objects.update_or_create(
                        codigo=codigo,
                        defaults={
                            'grupo':      grupo,
                            'subgrupo':   subg,
                            'nombre':     row['Producto'],
                            'iva':        row['Iva'],
                            'externo_id': str(row['id']),
                            'descuento':  row['Descuento'],
                            'precio1':    row['PRECIO 1'],
                            'precio2':    row['PRECIO 2'],
                            'precio3':    row['PRECIO 3'],
                            'precio4':    row['PRECIO 4'],
                            'precio5':    row['PRECIO 5'],
                            'precio6':    row['PRECIO 6'],
                            'stock':      nuevo_stock,
                        }
                    )

                    count += 1

                except Exception as e:
                    errors.append(f"Fila {idx+5}: {e}")

            return redirect('productos:import_success')

    else:
        form = UploadExcelForm()

    return render(request, 'productos/import.html', {
        'form':   form,
        'count':  count,
        'errors': errors,
    })


@login_required
def mis_productos(request):
    """
    Muestra los productos asignados al vendedor actual.
    """
    vendedor = get_object_or_404(Vendedor, user=request.user)
    productos = Producto.objects.filter(subgrupo__in=vendedor.subgrupos.all())
    return render(request, 'productos/mis_productos.html', {
        'productos': productos
    })


@login_required
def movimientos_stock(request, producto_id):
    """
    Historial de movimientos de stock para un producto dado.
    """
    prod = get_object_or_404(Producto, pk=producto_id)
    movimientos = prod.movimientos.all()  # gracias al related_name en el modelo
    return render(request, 'productos/movimientos.html', {
        'producto':    prod,
        'movimientos': movimientos,
    })

@login_required
def inventario_vendedor(request):
    """
    Muestra el inventario (productos + stock) asignado al vendedor logueado,
    junto al enlace al historial de cada producto.
    """
    vendedor = get_object_or_404(Vendedor, user=request.user)
    
    # Base de productos asignados al vendedor
    productos_base = Producto.objects.filter(subgrupo__in=vendedor.subgrupos.all())
    
    # Obtener los grupos y subgrupos únicos de los productos del vendedor
    grupos = Grupo.objects.filter(producto__in=productos_base).distinct().order_by('nombre')
    subgrupos = SubGrupo.objects.filter(producto__in=productos_base).distinct().order_by('nombre')

    # Leer parámetros GET de filtrado
    gid = request.GET.get('grupo')
    sgid = request.GET.get('subgrupo')

    # Filtrar productos
    productos_filtrados = productos_base
    if gid:
        productos_filtrados = productos_filtrados.filter(grupo_id=gid)
        # Si se filtra por grupo, los subgrupos a mostrar deben ser solo los de ese grupo
        subgrupos = subgrupos.filter(grupo_id=gid)
    if sgid:
        productos_filtrados = productos_filtrados.filter(subgrupo_id=sgid)

    # Crear el diccionario de filtro para la plantilla
    filtro = {
        'grupo': int(gid) if gid else None,
        'subgrupo': int(sgid) if sgid else None,
    }

    return render(request, 'productos/inventario_vendedor.html', {
        'productos': productos_filtrados,
        'grupos': grupos,
        'subgrupos': subgrupos,  # Pasamos la lista de subgrupos (potencialmente filtrada)
        'filtro': filtro
    })


def es_jefe_de_ventas(user):
    # Ajusta esta condición a tu lógica (por ejemplo, grupo 'jefeventas' o flag en el perfil)
    return user.groups.filter(name='jefeventas').exists()


@user_passes_test(es_jefe_de_ventas)
def inventario_jefe(request):
    """
    Muestra un formulario para filtrar por Grupo / SubGrupo / Vendedor,
    y luego lista los productos que coinciden con el filtro seleccionado.
    """
    grupos     = Grupo.objects.all().order_by('nombre')
    vendedores = Vendedor.objects.all().select_related('user')

    # Leer parámetros GET de filtrado
    gid = request.GET.get('grupo')
    sgid = request.GET.get('subgrupo')
    vid = request.GET.get('vendedor')

    qs = Producto.objects.all()

    if gid:
        qs = qs.filter(grupo_id=gid)
    if sgid:
        qs = qs.filter(subgrupo_id=sgid)
    if vid:
        # filtrar por subgrupos del vendedor elegido
        sel_v = Vendedor.objects.get(pk=vid)
        qs = qs.filter(subgrupo__in=sel_v.subgrupos.all())

    return render(request, 'productos/inventario_jefe.html', {
        'grupos':     grupos,
        'vendedores': vendedores,
        'productos':  qs.order_by('grupo__nombre','subgrupo__nombre','codigo'),
        'filtro': {
            'grupo':     int(gid) if gid else None,
            'subgrupo':  int(sgid) if sgid else None,
            'vendedor':  int(vid) if vid else None,
        }
    })
# 
# ============================================================================
# VISTAS DEL GESTOR
# ============================================================================

def es_gestor(user):
    """Verifica si el usuario es gestor"""
    return user.is_authenticated and user.groups.filter(name='Gestor').exists()

@user_passes_test(es_gestor, login_url='login')
def inventario_gestor(request):
    """Vista del inventario general para gestores con todos los grupos y subgrupos"""
    from django.db.models import Sum, Count
    
    # Obtener todos los grupos con sus subgrupos y productos
    grupos = Grupo.objects.prefetch_related(
        'subgrupo_set__producto_set'
    ).all().order_by('nombre')
    
    # Estadísticas generales
    total_productos = Producto.objects.count()
    productos_sin_stock = Producto.objects.filter(stock=0).count()
    productos_stock_bajo = Producto.objects.filter(stock__lte=10, stock__gt=0).count()
    valor_total_inventario = Producto.objects.aggregate(
        total=Sum('precio1')
    )['total'] or 0
    
    # Filtros
    filtro_grupo = request.GET.get('grupo', '')
    filtro_subgrupo = request.GET.get('subgrupo', '')
    filtro_stock = request.GET.get('stock', '')
    
    # Aplicar filtros si existen
    productos = Producto.objects.select_related('grupo', 'subgrupo').all()
    
    if filtro_grupo:
        productos = productos.filter(grupo__id=filtro_grupo)
        grupos = grupos.filter(id=filtro_grupo)
    
    if filtro_subgrupo:
        productos = productos.filter(subgrupo__id=filtro_subgrupo)
    
    if filtro_stock == 'sin_stock':
        productos = productos.filter(stock=0)
    elif filtro_stock == 'stock_bajo':
        productos = productos.filter(stock__lte=10, stock__gt=0)
    elif filtro_stock == 'con_stock':
        productos = productos.filter(stock__gt=10)
    
    productos = productos.order_by('grupo__nombre', 'subgrupo__nombre', 'codigo')
    
    # Paginación
    from django.core.paginator import Paginator
    paginator = Paginator(productos, 50)  # 50 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'grupos': grupos,
        'page_obj': page_obj,
        'total_productos': total_productos,
        'productos_sin_stock': productos_sin_stock,
        'productos_stock_bajo': productos_stock_bajo,
        'valor_total_inventario': valor_total_inventario,
        'filtros': {
            'grupo': filtro_grupo,
            'subgrupo': filtro_subgrupo,
            'stock': filtro_stock,
        },
        'todos_los_grupos': Grupo.objects.all().order_by('nombre'),
        'todos_los_subgrupos': SubGrupo.objects.all().order_by('nombre'),
    }
    
    return render(request, 'productos/inventario_gestor.html', context)

@user_passes_test(es_gestor, login_url='login')
def subir_bd_productos_gestor(request):
    """Vista para que el gestor suba base de datos de productos por grupo/subgrupo"""
    import json
    from django.http import JsonResponse
    from django.contrib import messages
    
    if request.method == 'POST':
        # Función temporalmente deshabilitada - requiere pandas
        messages.error(request, "Función de importación temporalmente deshabilitada. Contacte al administrador.")
        return redirect('productos:inventario_gestor')
        
        # TODO: Implementar importación sin pandas o agregar pandas al requirements.txt
        """
        try:
            # Procesar archivo subido
            archivo = request.FILES.get('archivo_productos')
            grupo_id = request.GET.get('grupo')
            subgrupo_id = request.GET.get('subgrupo')
            
            if not archivo:
                return JsonResponse({'error': 'No se seleccionó archivo'}, status=400)
            
            # Leer archivo Excel
            df = pd.read_excel(archivo, header=4, engine='openpyxl').fillna(0)
            
            productos_procesados = 0
            productos_actualizados = 0
            productos_nuevos = 0
            errores = []
            
            for idx, row in df.iterrows():
                try:
                    # Obtener o crear grupo y subgrupo
                    if grupo_id:
                        grupo = Grupo.objects.get(id=grupo_id)
                    else:
                        grupo, _ = Grupo.objects.get_or_create(nombre=row['Grupo'])
                    
                    if subgrupo_id:
                        subgrupo = SubGrupo.objects.get(id=subgrupo_id)
                    else:
                        subgrupo, _ = SubGrupo.objects.get_or_create(
                            nombre=row['Sub Grupo'],
                            grupo=grupo
                        )
                    
                    # Procesar producto
                    codigo = str(row['codigo']).strip()
                    
                    # Verificar si existe
                    producto_existente = Producto.objects.filter(codigo=codigo).first()
                    
                    # Crear o actualizar producto
                    producto, created = Producto.objects.update_or_create(
                        codigo=codigo,
                        defaults={
                            'grupo': grupo,
                            'subgrupo': subgrupo,
                            'nombre': row['Producto'],
                            'iva': row['Iva'],
                            'externo_id': str(row['id']),
                            'descuento': row['Descuento'],
                            'precio1': row['PRECIO 1'],
                            'precio2': row['PRECIO 2'],
                            'precio3': row['PRECIO 3'],
                            'precio4': row['PRECIO 4'],
                            'precio5': row['PRECIO 5'],
                            'precio6': row['PRECIO 6'],
                            'stock': int(row['stock']),
                        }
                    )
                    
                    if created:
                        productos_nuevos += 1
                    else:
                        productos_actualizados += 1
                    
                    productos_procesados += 1
                    
                    # Crear movimiento de stock si es necesario
                    if producto_existente and producto_existente.stock != int(row['stock']):
                        diferencia = int(row['stock']) - producto_existente.stock
                        StockMovimiento.objects.create(
                            producto=producto,
                            tipo='ENT' if diferencia > 0 else 'SAL',
                            cantidad=abs(diferencia),
                            responsable=request.user,
                            notas=f'Actualización masiva - Gestor: {request.user.username}'
                        )
                
                except Exception as e:
                    errores.append(f"Fila {idx+5}: {str(e)}")
            
            # Preparar respuesta
            resultado = {
                'success': True,
                'productos_procesados': productos_procesados,
                'productos_nuevos': productos_nuevos,
                'productos_actualizados': productos_actualizados,
                'errores': errores,
                'total_errores': len(errores)
            }
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(resultado)
            else:
                messages.success(request, f'Procesados {productos_procesados} productos exitosamente')
                return redirect('productos:subir_bd_productos_gestor')
                
        except Exception as e:
            error_msg = f'Error al procesar archivo: {str(e)}'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': error_msg}, status=500)
            else:
                messages.error(request, error_msg)
    
    # Obtener grupos y subgrupos para el formulario
    grupos = Grupo.objects.prefetch_related('subgrupo_set').all().order_by('nombre')
    
    # Estadísticas actuales
    total_productos = Producto.objects.count()
    productos_sin_stock = Producto.objects.filter(stock=0).count()
    
    context = {
        'grupos': grupos,
        'total_productos': total_productos,
        'productos_sin_stock': productos_sin_stock,
    }
    
    return render(request, 'productos/subir_bd_productos_gestor.html', context)

@user_passes_test(es_gestor, login_url='login')
def actualizar_bd_productos_gestor(request):
    """Vista para que el gestor actualice la base de datos de productos"""
    from .models import Producto, Grupo, SubGrupo
    from django.http import JsonResponse
    from django.contrib import messages
    from django.shortcuts import redirect, render
    from decimal import Decimal, InvalidOperation
    # import pandas as pd  # Comentado temporalmente
    
    # Mensaje de debug simple que siempre se muestra
    print(f"FUNCIÓN EJECUTADA - Método: {request.method}")
    
    if request.method == 'POST':
        # Verificar si es una petición AJAX
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        # Obtener datos del formulario
        archivo = request.FILES.get('archivo_productos')
        modo_actualizacion = request.POST.get('modo_actualizacion', 'actualizar')
        crear_grupos = request.POST.get('crear_grupos') == 'on'
        crear_subgrupos = request.POST.get('crear_subgrupos') == 'on'
        validar_precios = request.POST.get('validar_precios') == 'on'
        
        # Verificar si se recibió archivo
        if not archivo:
            error_msg = 'No se seleccionó archivo'
            if is_ajax:
                return JsonResponse({'error': error_msg}, status=400)
            else:
                messages.error(request, error_msg)
                return redirect('productos:actualizar_bd_clientes_gestor')
        
        # Quitar la respuesta de prueba y usar la función real
        
        try:
            # Función temporalmente deshabilitada - requiere pandas
            error_msg = 'Función de importación temporalmente deshabilitada. Pandas no está instalado.'
            if is_ajax:
                return JsonResponse({'error': error_msg}, status=400)
            else:
                messages.error(request, error_msg)
                return redirect('productos:inventario_gestor')
            
            # TODO: Implementar importación sin pandas o agregar pandas al requirements.txt
            """
            # Código original comentado hasta agregar pandas:
            if archivo.name.endswith('.xlsx'):
                df = pd.read_excel(archivo, engine='openpyxl', header=4).fillna('')
            else:  # CSV
                df = pd.read_csv(archivo, header=4).fillna('')"""
            
            # Información del archivo para debug
            info_debug = {
                'filas_leidas': len(df),
                'columnas_disponibles': list(df.columns),
                'primera_fila': df.iloc[0].to_dict() if len(df) > 0 else None
            }
            
            print(f"DEBUG: Archivo leído con {len(df)} filas")
            print(f"DEBUG: Columnas disponibles: {list(df.columns)}")
            print(f"DEBUG: Columnas con repr: {[repr(col) for col in df.columns]}")
            if len(df) > 0:
                print(f"DEBUG: Primera fila completa: {df.iloc[0].to_dict()}")
                print(f"DEBUG: Primeras 5 filas de columnas clave:")
                for i in range(min(5, len(df))):
                    row = df.iloc[i]
                    print(f"  Fila {i}: codig='{row.get('codig')}', Grup='{row.get('Grup')}', Sub Grup='{row.get('Sub Grup')}'")
                    # Intentar con nombres alternativos
                    for col in df.columns:
                        if 'grup' in col.lower() or 'group' in col.lower():
                            print(f"    Columna '{col}': '{row.get(col)}'")
                        if 'codig' in col.lower() or 'codigo' in col.lower():
                            print(f"    Columna '{col}': '{row.get(col)}'")
                        if 'sub' in col.lower():
                            print(f"    Columna '{col}': '{row.get(col)}'")
            
            productos_procesados = 0
            productos_nuevos = 0
            productos_actualizados = 0
            grupos_creados = 0
            subgrupos_creados = 0
            errores = []
            
            # Variables para recordar los últimos valores válidos (para celdas combinadas)
            ultimo_codigo_valido = ""
            ultimo_grupo_valido = ""
            ultimo_subgrupo_valido = ""
            
            for idx, row in df.iterrows():
                try:
                    # Validaciones básicas - usar nombres exactos de columnas del Excel
                    codigo_raw = str(row.get('codigo', '')).strip()
                    nombre = str(row.get('Producto', '')).strip()
                    grupo_raw = str(row.get('Grupo', '')).strip()
                    subgrupo_raw = str(row.get('Sub Grupo', '')).strip()
                    
                    # Manejar celdas combinadas: usar valores anteriores si están vacíos
                    if codigo_raw and codigo_raw != 'nan':
                        ultimo_codigo_valido = codigo_raw
                        codigo = codigo_raw
                    else:
                        codigo = ultimo_codigo_valido
                    
                    if grupo_raw and grupo_raw != 'nan':
                        ultimo_grupo_valido = grupo_raw
                        grupo_nombre = grupo_raw
                    else:
                        grupo_nombre = ultimo_grupo_valido
                    
                    if subgrupo_raw and subgrupo_raw != 'nan':
                        ultimo_subgrupo_valido = subgrupo_raw
                        subgrupo_nombre = subgrupo_raw
                    else:
                        subgrupo_nombre = ultimo_subgrupo_valido
                    
                    print(f"DEBUG Fila {idx+1}: Codigo='{codigo}' (raw='{codigo_raw}'), Nombre='{nombre}', Grupo='{grupo_nombre}' (raw='{grupo_raw}'), Subgrupo='{subgrupo_nombre}' (raw='{subgrupo_raw}')")
                    
                    # Saltar filas de totales o filas vacías (como la última fila del Excel)
                    if codigo_raw == 'nan' and nombre == 'nan':
                        print(f"DEBUG: Saltando fila {idx+1} - parece ser fila de totales")
                        continue
                    
                    # Validar que tengamos todos los campos necesarios
                    if not codigo or not nombre:
                        errores.append(f"Fila {idx+2}: Faltan campos críticos - Codigo='{codigo}', Nombre='{nombre}'")
                        continue
                    
                    if not grupo_nombre or not subgrupo_nombre:
                        errores.append(f"Fila {idx+2}: Faltan grupo/subgrupo - Grupo='{grupo_nombre}', Subgrupo='{subgrupo_nombre}'")
                        continue
                    
                    # Obtener o crear grupo
                    if crear_grupos:
                        grupo, grupo_creado = Grupo.objects.get_or_create(
                            nombre=grupo_nombre
                        )
                        if grupo_creado:
                            grupos_creados += 1
                            print(f"DEBUG: Grupo creado: {grupo_nombre}")
                    else:
                        try:
                            grupo = Grupo.objects.get(nombre=grupo_nombre)
                        except Grupo.DoesNotExist:
                            errores.append(f"Fila {idx+2}: El grupo '{grupo_nombre}' no existe y la creación automática está deshabilitada")
                            continue
                    
                    # Obtener o crear subgrupo
                    if crear_subgrupos:
                        subgrupo, subgrupo_creado = SubGrupo.objects.get_or_create(
                            nombre=subgrupo_nombre,
                            grupo=grupo
                        )
                        if subgrupo_creado:
                            subgrupos_creados += 1
                            print(f"DEBUG: Subgrupo creado: {subgrupo_nombre} en {grupo_nombre}")
                    else:
                        try:
                            subgrupo = SubGrupo.objects.get(nombre=subgrupo_nombre, grupo=grupo)
                        except SubGrupo.DoesNotExist:
                            errores.append(f"Fila {idx+2}: El subgrupo '{subgrupo_nombre}' no existe en el grupo '{grupo_nombre}' y la creación automática está deshabilitada")
                            continue
                    
                    # Procesar campos numéricos
                    def procesar_decimal(valor, nombre_campo, default=0):
                        try:
                            if valor == '' or valor is None:
                                return Decimal(str(default))
                            return Decimal(str(valor))
                        except (InvalidOperation, ValueError):
                            if validar_precios:
                                raise ValueError(f"{nombre_campo} inválido: {valor}")
                            return Decimal(str(default))
                    
                    def procesar_entero(valor, nombre_campo, default=0):
                        try:
                            if valor == '' or valor is None:
                                return default
                            return int(float(valor))
                        except (ValueError, TypeError):
                            if validar_precios:
                                raise ValueError(f"{nombre_campo} inválido: {valor}")
                            return default
                    
                    # Procesar datos del producto - usar nombres exactos de columnas del Excel
                    iva = procesar_decimal(row.get('Iva', 0), 'Iva')
                    descuento = procesar_decimal(row.get('Descuento', 0), 'Descuento')
                    precio1 = procesar_decimal(row.get('PRECIO 1', 0), 'PRECIO 1')
                    precio2 = procesar_decimal(row.get('PRECIO 2', 0), 'PRECIO 2')
                    precio3 = procesar_decimal(row.get('PRECIO 3', 0), 'PRECIO 3')
                    precio4 = procesar_decimal(row.get('PRECIO 4', 0), 'PRECIO 4')
                    precio5 = procesar_decimal(row.get('PRECIO 5', 0), 'PRECIO 5')
                    precio6 = procesar_decimal(row.get('PRECIO 6', 0), 'PRECIO 6')
                    stock = procesar_entero(row.get('stock', 0), 'stock')
                    externo_id = str(row.get('id', '')).strip()
                    
                    # Verificar si existe el producto
                    producto_existente = Producto.objects.filter(codigo=codigo).first()
                    
                    if producto_existente:
                        if modo_actualizacion in ['actualizar', 'solo_actualizar']:
                            producto_existente.grupo = grupo
                            producto_existente.subgrupo = subgrupo
                            producto_existente.nombre = nombre
                            producto_existente.iva = iva
                            producto_existente.descuento = descuento
                            producto_existente.precio1 = precio1
                            producto_existente.precio2 = precio2
                            producto_existente.precio3 = precio3
                            producto_existente.precio4 = precio4
                            producto_existente.precio5 = precio5
                            producto_existente.precio6 = precio6
                            producto_existente.stock = stock
                            producto_existente.externo_id = externo_id
                            producto_existente.save()
                            productos_actualizados += 1
                            print(f"DEBUG: Producto actualizado: {codigo}")
                        # Si es 'solo_nuevos', no hacer nada
                    else:
                        if modo_actualizacion in ['actualizar', 'solo_nuevos']:
                            nuevo_producto = Producto.objects.create(
                                grupo=grupo,
                                subgrupo=subgrupo,
                                codigo=codigo,
                                nombre=nombre,
                                iva=iva,
                                descuento=descuento,
                                precio1=precio1,
                                precio2=precio2,
                                precio3=precio3,
                                precio4=precio4,
                                precio5=precio5,
                                precio6=precio6,
                                stock=stock,
                                externo_id=externo_id
                            )
                            productos_nuevos += 1
                            print(f"DEBUG: Producto creado: {codigo}")
                    
                    productos_procesados += 1
                    
                except Exception as e:
                    error_msg = f"Fila {idx+2}: {str(e)}"
                    errores.append(error_msg)
                    print(f"DEBUG ERROR: {error_msg}")
            
            print(f"DEBUG FINAL: Procesados={productos_procesados}, Nuevos={productos_nuevos}, Actualizados={productos_actualizados}")
            print(f"DEBUG FINAL: Grupos creados={grupos_creados}, Subgrupos creados={subgrupos_creados}")
            
            # Preparar respuesta
            resultado = {
                'success': True,
                'productos_procesados': productos_procesados,
                'productos_nuevos': productos_nuevos,
                'productos_actualizados': productos_actualizados,
                'grupos_creados': grupos_creados,
                'subgrupos_creados': subgrupos_creados,
                'errores': errores,
                'total_errores': len(errores),
                'debug_info': info_debug  # Agregar información de debug
            }
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(resultado)
            else:
                messages.success(request, f'Procesados {productos_procesados} productos exitosamente')
                return redirect('productos:actualizar_bd_clientes_gestor')
                
        except Exception as e:
            error_msg = f'Error al procesar archivo: {str(e)}'
            print(f"DEBUG ERROR GENERAL: {error_msg}")
            if is_ajax:
                return JsonResponse({'error': error_msg}, status=500)
            else:
                messages.error(request, error_msg)
                return redirect('productos:actualizar_bd_clientes_gestor')
    
    # Estadísticas actuales
    total_productos = Producto.objects.count()
    total_grupos = Grupo.objects.count()
    total_subgrupos = SubGrupo.objects.count()
    
    context = {
        'total_productos': total_productos,
        'total_grupos': total_grupos,
        'total_subgrupos': total_subgrupos,
    }
    
    return render(request, 'productos/actualizar_bd_clientes_gestor.html', context)