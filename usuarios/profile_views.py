from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import UserProfile
import os

class ProfileForm(forms.ModelForm):
    """Formulario para actualizar información del perfil"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False, label='Nombre')
    last_name = forms.CharField(max_length=30, required=False, label='Apellido')
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors'
            })

class ProfilePictureForm(forms.Form):
    """Formulario para subir foto de perfil"""
    profile_picture = forms.ImageField(
        required=True,
        label='Foto de Perfil',
        widget=forms.FileInput(attrs={
            'class': 'hidden',
            'accept': 'image/*'
        })
    )
    
    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError('La imagen no puede ser mayor a 5MB.')
            if not picture.content_type.startswith('image/'):
                raise forms.ValidationError('El archivo debe ser una imagen.')
        return picture

@login_required
def profile_view(request):
    """Vista principal del perfil de usuario"""
    context = {
        'user': request.user,
        'profile_form': ProfileForm(instance=request.user),
        'picture_form': ProfilePictureForm(),
        'password_form': PasswordChangeForm(request.user),
    }
    return render(request, 'usuarios/profile.html', context)

@login_required
def update_profile(request):
    """Actualizar información básica del perfil"""
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    return redirect('usuarios:profile')

@login_required
def change_password(request):
    """Cambiar contraseña del usuario"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantener la sesión activa
            messages.success(request, 'Tu contraseña ha sido cambiada correctamente.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    return redirect('usuarios:profile')

@login_required
def upload_profile_picture(request):
    """Subir foto de perfil"""
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data['profile_picture']
            
            # Crear directorio si no existe
            profile_dir = f'profile_pictures/{request.user.id}/'
            if not default_storage.exists(profile_dir):
                default_storage.save(profile_dir + '.keep', ContentFile(''))
            
            # Eliminar foto anterior si existe
            old_pictures = default_storage.listdir(profile_dir)[1]  # [1] son los archivos
            for old_pic in old_pictures:
                if old_pic != '.keep':
                    default_storage.delete(profile_dir + old_pic)
            
            # Guardar nueva foto
            filename = f'profile_{request.user.id}.{picture.name.split(".")[-1]}'
            file_path = profile_dir + filename
            default_storage.save(file_path, picture)
            
            # Guardar ruta en el perfil del usuario (necesitaremos crear un modelo Profile)
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.profile_picture = file_path
            profile.save()
            
            messages.success(request, 'Tu foto de perfil ha sido actualizada.')
        else:
            for error in form.errors.values():
                messages.error(request, error[0])
    
    return redirect('usuarios:profile')

