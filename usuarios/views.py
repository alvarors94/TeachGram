from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from .forms import FormularioLogin
from django.utils.decorators import method_decorator #Para añadir decoradores
from django.views.decorators.cache import never_cache #Para que no guarde los datos en cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login


class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = '/'
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        """
        This function is a decorator that is used to protect the view from Cross-Site Request Forgery (CSRF) attacks.
        It is used by adding the @csrf_protect decorator to the view function.
        The @csrf_protect decorator adds a hidden form field to the response that is used to verify that the request is
        legitimate.

        The @never_cache decorator is used to prevent the view from being cached by the browser. This is because the
        CSRF protection requires that the view be posted, and cached pages cannot be posted.

        The function checks if the user is already authenticated. If the user is authenticated, it redirects them to the
        success_url. If the user is not authenticated, it calls the parent dispatch function.

        Args:
            request (HttpRequest): The HTTP request object.
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The HTTP response object.
        """
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)
            
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)