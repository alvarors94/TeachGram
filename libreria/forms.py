from django import forms
from .models import Publicacion, Comentario, Perfil
from django.contrib.auth.models import User

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['foto_publicacion', 'descripcion']
        
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario']  # Campos del formulario
        
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['profile_pic']  
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username' ,'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            # 'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

       