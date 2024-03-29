from django import forms
from .models import Publicacion, Comentario, Perfil, Recursos, Imagen, Iframe
from django.contrib.auth.models import User
import re

class PublicacionForm(forms.ModelForm):
    descripcion = forms.CharField(required=False, help_text='Añada una descripción... (máx. 200 caracteres)')

    def clean(self):
        cleaned_data = super().clean()
        descripcion = cleaned_data.get('descripcion')

        if descripcion and len(descripcion) > 200:
            self.add_error('descripcion', f'El límite de caracteres para este campo es de 200 y tiene {len(descripcion)}')
        elif not descripcion:
            self.add_error('descripcion', 'Este campo no puede estar vacío')

        return cleaned_data
    
    class Meta:
        model = Publicacion
        fields = ['descripcion']
        
class ImagenForm(forms.ModelForm):
    
    widgets = {'imagen': forms.ImageField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}))}
    required = False
    help_text = 'Puede añadir una o varias imágenes'
    class Meta:
        model = Imagen
        fields = ['imagen']
        
        
class ComentarioForm(forms.ModelForm):
    comentario = forms.CharField(required=False ,help_text = 'Escriba su comentario)')

    def clean_comentario(self):
        comentario = self.cleaned_data.get('comentario')
        if len(comentario) > 400:
            raise forms.ValidationError('El comentario no puede tener más de 400 caracteres')
        return comentario

    class Meta:
        model = Comentario
        fields = ['comentario']  # Campos del formulario
        
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['profile_pic']  


class UserForm(forms.ModelForm):
    username = forms.CharField(required=False, label="Nombre de usuario")
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Contraseña")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            self.add_error('username', 'El nombre de usuario no puede estar vacío')

        if not password:
            self.add_error('password', 'La contraseña no puede estar vacía')

        # Llamar al método para verificar si el nombre de usuario ya existe
       
        return cleaned_data
    


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
    archivo_recurso = forms.FileField(required=False, label="Archivo", help_text = "Puedes subir cualquier archivo, como 'pdf', 'word', imágenes ... ")
    nombre = forms.CharField(required=False)
    descripcion = forms.CharField(required=False,help_text = "Añada una descripción... (máx. 400 caracteres) ")
   
                                                                                                                                  

    def clean(self):
        cleaned_data = super().clean()
        archivo_recurso = cleaned_data.get('archivo_recurso')
        nombre = cleaned_data.get('nombre')
        descripcion = cleaned_data.get('descripcion')

        if not archivo_recurso:
            self.add_error('archivo_recurso', 'Este campo no puede estar vacío')
            
        if not nombre:
            self.add_error('nombre', 'Este campo no puede estar vacío')
            
        if nombre and len(nombre) > 200:
            self.add_error('nombre', f'El límite de caracteres para este campo es de 200 y tiene {len(nombre)}')
            
        if not descripcion:
            self.add_error('descripcion', 'Este campo no puede estar vacío')
        
        if descripcion and len(descripcion) > 400:
            self.add_error('descripcion', f'El límite de caracteres para este campo es de 400 y tiene {len(descripcion)}')

        return cleaned_data

    class Meta:
        model = Recursos
        fields = ['archivo_recurso', 'nombre','descripcion']
        

class IframeForm(forms.ModelForm):
    codigo_iframe = forms.CharField(required=False, label="Código Iframe", help_text = 'Por ejemplo <iframe width="560" height="315" src="https://www.youtube.com/embed/...></iframe>')
    descripcion = forms.CharField(required=False, help_text = 'Añada una descripción... (máx. 400 caracteres)')
    
    def clean(self):
        cleaned_data = super().clean()
        codigo_iframe = cleaned_data.get('codigo_iframe')
        descripcion = cleaned_data.get('descripcion')

        if not codigo_iframe:
            self.add_error('codigo_iframe', 'Este campo no puede estar vacío')
            
        if descripcion and len(descripcion) > 400:
            self.add_error('descripcion', f'El límite de caracteres para este campo es de 400 y tiene {len(descripcion)}')
            
        if not "<iframe " in codigo_iframe:
            self.add_error('codigo_iframe', 'Este formato de código no es válido, debe empezar por <iframe ...')
            
        return cleaned_data

    class Meta:
        model = Iframe
        fields = ['codigo_iframe', 'descripcion']