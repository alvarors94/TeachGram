from .models import Perfil

def foto_perfil(request):
    foto_perfil = None
    if request.user.is_authenticated:
        perfil = Perfil.objects.get(username=request.user)
        foto_perfil = perfil.profile_pic.url if perfil else None
    return {'foto_perfil': foto_perfil}