# def crear_publicacion(request):
#     if request.method == 'POST':
#         form_publicacion = PublicacionForm(request.POST, request.FILES)
#         if form_publicacion.is_valid():
#             publicacion = form_publicacion.save(commit=False)
#             publicacion.user_id = request.user.id  # Asigna el id del usuario autenticado
#             publicacion.save()
#             return redirect("publicaciones")
#     else:
#         form_publicacion = PublicacionForm()
    
#     return render(request, "perfil/crear_publicacion.html", {"form_publicacion": form_publicacion})