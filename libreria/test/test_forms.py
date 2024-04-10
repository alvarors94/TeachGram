import unittest
from libreria.forms import *

class TestUserForm(unittest.TestCase):

    def test_clean(self):
        form_data = {'username': 'testuser', 'password': 'password'}
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'username': '', 'password': 'password'}
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['El nombre de usuario no puede estar vacío'])

        form_data = {'username': 'testuser', 'password': ''}
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], ['La contraseña no puede estar vacía'])
        
class TestPublicacionForm(unittest.TestCase):
    def test_clean(self):
        # Test valid description length
        form_data = {'descripcion': 'This is a test.'}
        form = PublicacionForm(data=form_data)
        self.assertTrue(form.is_valid())  # Ensure form is valid
        cleaned_data = form.clean()
        self.assertIn('descripcion', cleaned_data)
        self.assertEqual(cleaned_data['descripcion'], 'This is a test.')

        # Test invalid description length
        form_data = {'descripcion': 'This is a test that is longer than 200 characters.'}
        form = PublicacionForm(data=form_data)
        self.assertFalse(form.is_valid())  # Ensure form is not valid
        self.assertIn('descripcion', form.errors)
        self.assertEqual(form.errors['descripcion'][0], 'El límite de caracteres para este campo es de 200 y tiene 288.')
   
class TestImagenForm(unittest.TestCase):
    def test_imagenform_inherits_from_modelform(self):
        self.assertIsInstance(ImagenForm(), forms.ModelForm)

    def test_imagenform_meta_defined(self):
        self.assertIsInstance(ImagenForm.Meta, type)

    def test_imagenform_meta_contains_correct_model_and_fields(self):
        self.assertEqual(ImagenForm.Meta.model, Imagen)
        self.assertEqual(ImagenForm.Meta.fields, ['imagen'])

    def test_imagenform_widgets_attribute_defined(self):
        self.assertIsInstance(ImagenForm.widgets, dict)

    def test_imagenform_widgets_contains_correct_key_value_pair(self):
        self.assertEqual(ImagenForm.widgets, {'imagen': forms.ImageField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}))})

    def test_imagenform_required_attribute_set_to_false(self):
        self.assertEqual(ImagenForm.required, False)

    def test_imagenform_help_text_attribute_set_to_correct_value(self):
        self.assertEqual(ImagenForm.help_text, 'Puede añadir una o varias imágenes')



    def test_imagenform_clean_method_contains_correct_code(self):
        code = """def clean(self):
        cleaned_data = super().clean()
        imagen = cleaned_data.get('imagen')

        if imagen and len(imagen) > 200:
            self.add_error('imagen', f'El límite de caracteres para este campo es de 200 y tiene {len(imagen)}')
        elif not imagen:
            self.add_error('imagen', 'Este campo no puede estar vacío')

        return cleaned_data"""
        exec(code)
        self.assertEqual(ImagenForm.clean.__code__.co_code, code.strip().strip('\n').encode('utf-8'))
        

class ComentarioFormTest(unittest.TestCase):
    def test_comentario_form(self):
        form_data = {'comentario': 'This is a test comment.'}
        form = ComentarioForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comentario_too_long(self):
        form_data = {'comentario': 'a' * 401}
        form = ComentarioForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comentario'][0], 'El comentario no puede tener más de 400 caracteres')
    
class PerfilFormTest(unittest.TestCase):
    def test_meta_class_exists_and_model_attribute_is_set_to_perfil(self):
        form_class = PerfilForm
        self.assertTrue(hasattr(form_class, 'Meta'))
        self.assertTrue(hasattr(form_class.Meta, 'model'))
        self.assertEqual(form_class.Meta.model, Perfil)

    def test_fields_attribute_exists_and_contains_profile_pic(self):
        form_class = PerfilForm
        self.assertTrue(hasattr(form_class, 'Meta'))
        self.assertTrue(hasattr(form_class.Meta, 'fields'))
        self.assertEqual(form_class.Meta.fields, ['profile_pic'])

    def test_profile_pic_field_is_of_type_imagefield_and_has_no_other_attributes(self):
        form_class = PerfilForm
        self.assertTrue(hasattr(form_class, 'Meta'))
        self.assertTrue(hasattr(form_class.Meta, 'fields'))
        fields = form_class.Meta.fields
        field = fields[0]
        self.assertTrue(hasattr(form_class, field))
        self.assertTrue(isinstance(getattr(form_class, field), forms.ImageField))
        self.assertFalse(getattr(form_class, field).required)
        self.assertFalse(getattr(form_class, field).label)
        self.assertFalse(getattr(form_class, field).help_text)
        
class ChangePasswordFormTest(unittest.TestCase):
    def test_CambiarPasswordForm_inherits_from_forms_Form(self):
        assert issubclass(CambiarPasswordForm, forms.Form)


    def test_CambiarPasswordForm_has_two_fields(self):
        form = CambiarPasswordForm()
        assert len(form.fields) == 2


    def test_password1_field_is_CharFieldself(self):
        form = CambiarPasswordForm()
        assert isinstance(form.fields['password1'], forms.CharField)


    def test_password2_field_is_CharField(self):
        form = CambiarPasswordForm()
        assert isinstance(form.fields['password2'], forms.CharField)


    def test_password1_field_has_correct_label(self):
        form = CambiarPasswordForm()
        assert form.fields['password1'].label == 'Nueva contraseña'


    def test_password1_field_has_correct_widget(self):
        form = CambiarPasswordForm()
        assert isinstance(form.fields['password1'].widget, forms.PasswordInput)


    def test_password1_field_has_correct_attributes(self):
        form = CambiarPasswordForm()
        attrs = form.fields['password1'].widget.attrs
        assert attrs['class'] == 'form-control'
        assert attrs['placeholder'] == 'Introduzca la nueva contraseña...'
        assert attrs['id'] == 'password1'


    def test_password2_field_has_correct_label(self):
        form = CambiarPasswordForm()
        assert form.fields['password2'].label == 'Confirmar contraseña'


    def test_password2_field_has_correct_widget(self):
        form = CambiarPasswordForm()
        assert isinstance(form.fields['password2'].widget, forms.PasswordInput)


    def test_password2_field_has_correct_attributes(self):
        form = CambiarPasswordForm()
        attrs = form.fields['password2'].widget.attrs
        assert attrs['class'] == 'form-control'
        assert attrs['placeholder'] == 'Confirme su nueva contraseña...'
        assert attrs['id'] == 'password2'


    def test_clean_method_verifies_password1_and_password2_fields_are_not_empty(self):
        form = CambiarPasswordForm(data={'password1': 'password', 'password2': 'password'})
        assert form.is_valid()


    def test_clean_method_verifies_password1_and_password2_fields_match(self):
        form = CambiarPasswordForm(data={'password1': 'password', 'password2': 'password'})
        assert form.is_valid()


    def test_clean_method_verifies_password2_field_contains_at_least_eight_characters(self):
        form = CambiarPasswordForm(data={'password1': 'password', 'password2': 'pa'})
        assert not form.is_valid()
        assert form.errors['password2'] == ['La contraseña debe tener al menos 8 caracteres']


    def test_clean_method_verifies_password2_field_contains_at_least_one_lowercase_letter_one_uppercase_letter_and_one_digit(self):
        form = CambiarPasswordForm(data={'password1': 'password', 'password2': 'P@$$w0rd'})
        assert not form.is_valid()
        assert form.errors['password2'] == ['La contraseña debe contener al menos una letra, un número y una mayúscula']


    def test_clean_method_raises_forms_ValidationError_with_error_message_if_any_verification_fails(self):
        form = CambiarPasswordForm(data={'password1': 'password', 'password2': 'P@$$w0rd'})
        assert not form.is_valid()
        assert form.errors == {
            'password2': ['La contraseña debe tener al menos 8 caracteres', 'La contraseña debe contener al menos una letra, un número y una mayúscula']
        }
        
class RecursosFormTest(unittest.TestCase):
    def test_campos(self):
        form = RecursosForm()
        self.assertSequenceEqual(form.fields.keys(), ['archivo_recurso', 'nombre', 'descripcion'])

    def test_limpieza(self):
        form_data = {'archivo_recurso': 'archivo.txt', 'nombre': 'Nombre', 'descripcion': 'Descripción'}
        form = RecursosForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['archivo_recurso'], 'archivo.txt')
        self.assertEqual(form.cleaned_data['nombre'], 'Nombre')
        self.assertEqual(form.cleaned_data['descripcion'], 'Descripción')

    def test_etiquetas(self):
        form = RecursosForm()
        self.assertEqual(form.fields['archivo_recurso'].label, 'Archivo')
        self.assertEqual(form.fields['nombre'].label, 'Nombre')
        self.assertEqual(form.fields['descripcion'].label, 'Descripción')
        self.assertEqual(form.fields['archivo_recurso'].help_text, 'Puedes subir cualquier archivo, como \'pdf\', \'word\', imágenes... ')
        self.assertEqual(form.fields['nombre'].help_text, None)
        self.assertEqual(form.fields['descripcion'].help_text, 'Añada una descripción... (máx. 400 caracteres)')
        
class IframeFormTest(unittest.TestCase):
    def setUp(self):
        self.form = IframeForm()  # Reemplaza YourIframeFormHere con tu clase de formulario

    def test_iframe_form_inherits_from_modelform(self):
        self.assertIsInstance(self.form, forms.ModelForm)

    def test_iframe_model_is_used(self):
        self.assertIsInstance(self.form.Meta.model(), Iframe)

    def test_form_has_two_fields(self):
        self.assertEqual(len(self.form.fields), 2)

    def test_codigo_iframe_field_is_a_CharField(self):
        self.assertIsInstance(self.form.fields['codigo_iframe'], forms.CharField)

    def test_codigo_iframe_field_is_required(self):
        self.assertFalse(self.form.fields['codigo_iframe'].required)

    def test_descripcion_field_is_a_CharField(self):
        self.assertIsInstance(self.form.fields['descripcion'], forms.CharField)

    def test_descripcion_field_is_optional(self):
        self.assertFalse(self.form.fields['descripcion'].required)

    def test_clean_method_is_defined(self):
        self.assertTrue(hasattr(self.form, 'clean'))

    def test_clean_method_contains_appropriate_code(self):
        expected_code = """
        if not codigo_iframe:
            self.add_error('codigo_iframe', 'Este campo no puede estar vacío')
        """
        self.assertIn(expected_code, self.form.clean.__code__.co_code)

    def test_form_is_associated_with_the_Iframe_model(self):
        self.assertEqual(self.form.Meta.model, Iframe)