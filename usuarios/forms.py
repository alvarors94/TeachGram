#Creamos un formulario para validar la informacion del login



from django.contrib.auth.forms import AuthenticationForm


class FormularioLogin(AuthenticationForm):
    def __init__(self,  *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['username'].widget.attrs['autofocus'] = True
        self.fields['password'].widget.attrs['autofocus'] = True
        self.fields['username'].widget.attrs['required'] = True
        self.fields['password'].widget.attrs['required'] = True
        self.fields['username'].widget.attrs['autofocus'] = True
        self.fields['password'].widget.attrs['autofocus'] = True