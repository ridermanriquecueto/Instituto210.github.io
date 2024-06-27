from re import template
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    #Usuarios del sistema   
    path('', HomePageView.as_view(), name= 'inicio'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("recuperar_pass/",auth_views.PasswordResetView.as_view(template_name="registration/recuperar_pass.html"),name='Recuperar Contraseña'),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_send.html"), name='password_reset_done'),
    path("create_user/",login_required(registerView.as_view(template_name= 'registration/register.html')), name='register'),
    path("career/", login_required(carreraView.as_view(template_name= 'carrera.html')), name='carrera'),
    path("institut/", login_required(carreraView.as_view(template_name= 'instituto.html')), name='instituto'),
    path("show_profile/", login_required(profileviews.as_view(template_name= 'registration/profile.html')), name='profile'),
    path("change_password/", auth_views.PasswordChangeView.as_view(template_name = 'registration/change_password.html'),name = 'cambiar_contraseña'),
    path("change_password_done/",auth_views.PasswordChangeDoneView.as_view(template_name='registration/success_password.html'), name='password_change_done'),
    path("user_list/",login_required(listUser.as_view(template_name='registration/list_user.html')),name='list_user'),
    path("edit_user/<int:pk>",login_required(editUser.as_view(template_name = 'registration/edit_profile.html')), name='edit_profile'),
    path("delete_user/<int:pk>",login_required(deleteUser.as_view(template_name='registration/delete_user.html')),name='delete_user'),
    path("show_user/<int:pk>",login_required(editUser.as_view(template_name = 'registration/show_user.html')), name='show_user'),
    #Alta e Inscripcion materias
    path('altaMateria/', login_required(alta_materia), name='altaMateria'),
    path('exito-alta-materia/', login_required(exito_alta_materia), name='exito_alta_materia'),
    path('lista_materias_user/', login_required(lista_materias_user), name='listaMateriasUser'),
    path('inscribirse_materia/<int:materia_id>', inscribirse_materia, name='inscribirse_materia'),
    path('alta_masiva_materia/', login_required(alta_masiva_materia), name= 'AltaMasivaMaterias'),
    path('editar_materia/<int:id>/', login_required(editar_materia), name='editar_materia'),
    path('exito_cambios_materia/', login_required(exito_cambios_materia), name='exito_cambios_materia'),
    path('alerta_materia_existente', login_required(alerta_materia_existente), name='alerta_materia_existente'),
    path('ver_materias/<int:id>/', ver_materias, name='ver_materias'),
    path('eliminar_materia/<int:id>/', login_required(eliminar_materia), name='eliminar_materia'),
    path('materias/eliminar_seleccionadas/', eliminar_materias_seleccionadas, name='eliminar_materias_seleccionadas'),
    path('exito_materia_eliminada/', exito_materia_eliminada, name='exito_materia_eliminada'),
    path('lista_materias_admin/', lista_materias_admin, name='lista_materias_admin'),
    #Alta e Inscripcion mesa de final Administrativo
    path('mesas_finales/', MesasFinalesListView.as_view(), name='mesas_finales_list'),
    path('inscribir_mesa_final/', inscribir_mesa_final, name='inscribir_mesa_final'),
    #Alta e Inscripcion mesa de final
    path('altaMesa/',altaMesa, name='altaMesa'),
    path("edit_mesa/<int:pk>",login_required(editMesa.as_view(template_name = 'registration/edit_mesa.html')), name='edit_mesa'),
    path('inscripcionMesa/',inscripcionMesa,name='inscripcionMesa'), 
    path('exito-inscripcion/', exito_inscripcion_final, name='exito_inscripcion_final'),
    path('exito_alta_mesa/', exito_alta_mesa, name='exito_alta_mesa'),
    path('inscripcionFinal/',inscripcionFinal, name='inscripcionFinal'),
    path("edit_inscr/<int:pk>",login_required(editInscr.as_view(template_name = 'registration/edit_inscr.html')), name='edit_inscr'),
    path('inscripcionFinal_est/',inscripcionFinal_est, name='inscripcionFinal_est'),
    path('exito_inscripcion_mesa/', exito_inscripcion_mesa, name='exito_inscripcion_mesa'),
    path('error_alta_mesa/', error_alta_mesa, name='error_alta_mesa'),
    path('error_inscripcion_adm/', error_inscripcion_adm, name='error_inscripcion_adm'),
    path('error_inscripcion_est/', error_inscripcion_est, name='error_inscripcion_est'),
    path("inscripcion_finales_lista/",login_required(listInscripcion.as_view(template_name='finales/list_inscripcion.html')),name='list_inscripcion'),
    path("mesas_lista/",login_required(listMesa.as_view(template_name='finales/list_mesa.html')),name='list_mesa'),
    path("delete_mesa/<int:pk>",login_required(deleteMesa.as_view(template_name='finales/delete_mesa.html')),name='delete_mesa'),
    path("delete_inscripcion/<int:pk>",login_required(deleteInscripcion.as_view(template_name='finales/delete_inscripcion.html')),name='delete_inscripcion'),
    #Estudiantes
    path('estudiantes/nuevo', EstudianteCreateView.as_view(), name='estudiante_nuevo'),
    path('estudiantes/<int:pk>/editar/', EstudianteUpdateView.as_view(), name='estudiante_editar'),
    path('estudiantes/<int:pk>/eliminar/', EstudianteDeleteView.as_view(), name='estudiante_eliminar'),
    path('cargaMasivaEstudiantes/',login_required(cargar_usuarios),name='cargaMasivaEstudiantes'),
    path('ver_usuario_materia/',listar_usuarios_materia,name='verUsuarioMateria'),
    

]
