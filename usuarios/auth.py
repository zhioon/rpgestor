from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

class RoleBasedLoginView(LoginView):
    """
    Tras validar credenciales, redirige según grupo de usuario.
    """
    def get_success_url(self):
        user = self.request.user
        
        # Log para depuración
        user_groups = [group.name for group in user.groups.all()]
        logger.info(f"Usuario {user.username} logueado con grupos: {user_groups}")
        
        # Verificar grupos en orden de prioridad
        if user.groups.filter(name='Vendedor').exists():
            logger.info(f"Redirigiendo usuario {user.username} a dashboard_vendedor")
            return reverse('usuarios:dashboard_vendedor')
        
        if user.groups.filter(name='JefeVentas').exists():
            logger.info(f"Redirigiendo usuario {user.username} a dashboard_jefeventas")
            return reverse('usuarios:dashboard_jefeventas')
        
        if user.groups.filter(name='Gestor').exists():
            logger.info(f"Redirigiendo usuario {user.username} a dashboard_gestor")
            return reverse('usuarios:dashboard_gestor')
        
        # Superusuarios al admin
        if user.is_superuser:
            logger.info(f"Redirigiendo superusuario {user.username} al admin")
            return reverse('admin:index')
        
        # Si no tiene grupos específicos, mostrar mensaje y usar fallback
        logger.warning(f"Usuario {user.username} no tiene grupos asignados")
        messages.warning(self.request, 'Tu usuario no tiene un rol específico asignado. Contacta al administrador.')
        
        # Fallback genérico
        return super().get_success_url()
    
    def form_valid(self, form):
        """Override para agregar logging adicional"""
        response = super().form_valid(form)
        user = form.get_user()
        logger.info(f"Login exitoso para usuario: {user.username}")
        return response
    
    def form_invalid(self, form):
        """Override para manejar errores de login"""
        logger.warning(f"Intento de login fallido desde IP: {self.request.META.get('REMOTE_ADDR')}")
        return super().form_invalid(form)
