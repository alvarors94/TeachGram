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
            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Nombre de usuario'}),
            # 'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Apellido'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Apellido'}),
        }

       
class CambiarPasswordForm(forms.Form):
    password1 = forms.CharField(label="Nueva contraseña", 
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Introduzca la nueva contraseña...',
                                                                  'id': 'password1',
                                                                  'required': 'required'})) 
    password2 = forms.CharField(label="Confirmar contraseña", 
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Confirme su nueva contraseña...',
                                                                  'id': 'password2',
                                                                  'required': 'required'})) 
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        elif len(password2) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres")
        return cleaned_data