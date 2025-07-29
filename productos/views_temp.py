"""
Funciones temporales para productos sin pandas
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

def es_gestor(user):
    """Verifica si el usuario es gestor"""
    return user.is_authenticated and user.groups.filter(name='Gestor').exists()

@user_passes_test(es_gestor, login_url='login')
def actualizar_bd_productos_gestor_temp(request):
    """Función temporal que reemplaza la función que usa pandas"""
    messages.error(request, "Función de importación temporalmente deshabilitada. Pandas no está instalado.")
    return redirect('productos:inventario_gestor')