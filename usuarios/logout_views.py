from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views import View

class CustomLogoutView(View):
    """
    Vista personalizada de logout que maneja tanto GET como POST
    """
    template_name = 'registration/logged_out.html'
    
    def get(self, request):
        """Manejar GET request - mostrar página de logout"""
        if request.user.is_authenticated:
            # Si el usuario está logueado, hacer logout automáticamente
            logout(request)
        
        # Mostrar la página de logout
        return render(request, self.template_name)
    
    def post(self, request):
        """Manejar POST request - logout tradicional"""
        logout(request)
        return render(request, self.template_name)