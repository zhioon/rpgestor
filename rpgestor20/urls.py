from django.contrib import admin
from django.urls import path, include
from core.views import export_tests
from usuarios.auth import RoleBasedLoginView
from usuarios.logout_views import CustomLogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# Importar vistas de error personalizadas
from core.error_views import custom_404_view, custom_500_view

# Vista para redireccionar la raíz al login
def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    # Redirección de la raíz al login
    path('', redirect_to_login, name='home'),
    
    path('accounts/login/',
         RoleBasedLoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('accounts/logout/',
         CustomLogoutView.as_view(),
         name='logout'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('export-tests/', export_tests, name='export_tests'),
    path('notificaciones/', include('notificaciones.urls', namespace='notificaciones')),
    path('insights/', include('insights.urls', namespace='insights')),
    path('clientes/', include('clientes.urls', namespace='clientes')),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('pedidos/',  include('pedidos.urls', namespace='pedidos')),
    path('productos/', include('productos.urls', namespace='productos')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # URL de prueba para página 404 (solo en desarrollo)
    urlpatterns += [
        path('test-404/', custom_404_view, {'exception': Exception('Test 404')}, name='test_404'),
    ]

# Configuración de vistas de error personalizadas
handler404 = custom_404_view
handler500 = custom_500_view