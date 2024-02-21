from django import forms
from .models import Publicacion, Comentario

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = "__all__"
        
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario']  # Campos del formulario

       