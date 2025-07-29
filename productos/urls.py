from django.urls import path
from . import views
from .views_temp import actualizar_bd_productos_gestor_temp

app_name = 'productos' 

urlpatterns = [
    path('mis-productos/', views.mis_productos, name='mis_productos'),
    path('inventario/vendedor/', views.inventario_vendedor, name='inventario_vendedor'),
    path('inventario/jefe/',      views.inventario_jefe,      name='inventario_jefe'),
    path('movimientos/<int:producto_id>/', views.movimientos_stock, name='movimientos_stock'),
    # path('import/', views.import_products, name='import_products'),  # Temporalmente deshabilitado
    
    # Vistas del Gestor (usando funciones temporales)
    path('gestor/inventario/', views.inventario_gestor, name='inventario_gestor'),
    # path('gestor/subir-bd-productos/', views.subir_bd_productos_gestor, name='subir_bd_productos_gestor'),  # Temporalmente deshabilitado
    path('gestor/actualizar-bd-clientes/', actualizar_bd_productos_gestor_temp, name='actualizar_bd_clientes_gestor'),
]
