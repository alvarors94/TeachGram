from django import forms
from .models import Publicacion, Comentario, Perfil, Recursos, Imagen
from django.contrib.auth.models import User
import re


class PublicacionForm(forms.ModelForm):
    descripcion = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        descripcion = cleaned_data.get('descripcion')

        if not descripcion:
            self.add_error('descripcion', 'Este campo no puede estar vacío')

        return cleaned_data
    
    class Meta:
        model = Publicacion
        fields = ['descripcion']
        
class ImagenForm(forms.ModelForm):
    
    widgets = {'imagen': forms.ImageField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}))}
    required = False
    class Meta:
        model = Imagen
        fields = ['imagen']
        
        
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario']  # Campos del formulario
        
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['profile_pic']  


class UserForm(forms.ModelForm):
    username = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            self.add_error('username', 'El nombre de usuario no puede estar vacío')

        if not password:
            self.add_error('password', 'La contraseña no puede estar vacía')

        # Llamar al método para verificar si el nombre de usuario ya existe
        self.check_username(username)

        return cleaned_data
    
    def check_username(self, username):
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'El nombre de usuario ya existe')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'password': 'Contraseña',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
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
        errors = []

        # Verificar si las contraseñas coinciden
        if password1 and password2 and password1 != password2:
            errors.append("Las contraseñas no coinciden")

        # Verificar si la contraseña tiene al menos 8 caracteres
        if len(password2) < 8:
            errors.append("La contraseña debe tener al menos 8 caracteres")

        # Verificar si la contraseña contiene al menos una letra minúscula, una letra mayúscula y un dígito
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', password2):
            errors.append("La contraseña debe contener al menos una letra, un número y una mayúscula")

        # Si hay errores, lanzar una excepción con los mensajes de error
        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data
    
class RecursosForm(forms.ModelForm):
    class Meta:
        model = Recursos
        fields = ['archivo_recurso', 'nombre','descripcion'] 
        


