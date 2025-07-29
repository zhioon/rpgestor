from django.urls import path
from . import views

app_name = 'insights'

urlpatterns = [
    path('',                         views.dashboard,               name='dashboard'),
    path('api/ventas/',              views.api_ventas,              name='api_ventas'),
    path('api/proyeccion/',          views.api_proyeccion,          name='api_proyeccion'),
    path('api/ventas/vendedor/',     views.api_ventas_por_vendedor, name='api_ventas_vendedor'),
    path('api/ventas/producto/',     views.api_ventas_por_producto, name='api_ventas_producto'),
    path('api/ventas/grupo-subgrupo/', views.api_ventas_por_grupo_subgrupo,
         name='api_ventas_grupo_subgrupo'),
    path('api/ventas/grupo/', views.api_ventas_por_grupo, name='api_ventas_por_grupo'),
    path('api/ventas/diarias-vendedor/',  views.api_ventas_diarias_vendedor,  name='api_v_diarias_v'),
    path('api/top-productos-vendedor/',   views.api_top_productos_vendedor,   name='api_top_prod_v'),
    path('api/bottom-productos-vendedor/',views.api_bottom_productos_vendedor,name='api_bot_prod_v'),
    path('api/presupuesto-vendedor/',     views.api_presupuesto_vendedor,     name='api_presupuesto_v'),
]
