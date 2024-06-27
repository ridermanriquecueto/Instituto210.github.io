
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView    
from .models import *
from .forms import *
from django.views.generic import CreateView,TemplateView,ListView,UpdateView,DeleteView
from django.core.mail import send_mail
from django.contrib.auth import *
from django.contrib import messages
from django.db.models import Q
from django import forms
from django.http import HttpResponse
import csv
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.paginator import *
from django.db import IntegrityError

# Create your views here.

class ArchivoForm(forms.Form):
    archivo_csv = forms.FileField(label = 'Seleccione un archivo csv', required=False)

class HomePageView(TemplateView):
    template_name = 'index.html'
    model=Usuario

    def get(self, request):
        return  render(request, 'index.html')
    

class CustomLoginView(LoginView):
  pass

       
class CustomLogoutView(LogoutView):

    def get(self,request):
        logout(request)
        messages.success(request, 'Su sesión se ha cerrado correctamente. Hasta la próxima!')
        return redirect("/")



class registerView(CreateView):
    
    model = Usuario
    form_class = registri_user_form
    

    def form_valid(self, form):
        
        usuario = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        password = form.cleaned_data.get('password2')
        usuario = authenticate(email=email, password=password)
    
        
        form.save()
        #login(self.request, usuario)
        
        #send_mail('subject', f'\n-Su Usuario es: {email} \n- Su contraseña es: {password}\nLink para cambiar contraseña es: http://http://127.0.0.1:8000/change_password/<int:pk>,',from_email='webmaster.isfdyt210@gmail.com',recipient_list = [email])
        
        return redirect('/user_list')
    

   
       
class editUser(UpdateView):
    model = Usuario
    form_class = profile_students_form
    template_name = 'registration/edit_profile.html'
    success_url = '/'
    
class editMesa(UpdateView):
    model = MesaFinal
    form_class = MesaFinalForm
    template_name = 'registration/edit_mesa.html'
    success_url = '/'
    
class editInscr(UpdateView):
    model = InscripcionFinal
    form_class = InscripcionFinalForm
    template_name = 'registration/edit_inscr.html'
    success_url = '/'
    
     
class profileviews(TemplateView):
    model = Usuario 
  

class deleteUser(DeleteView):
    model = Usuario
    template_name ='registration/delete_user.html'
    success_url = '/user_list'
    
class deleteInscripcion(DeleteView):
    model = InscripcionFinal
    template_name ='registration/delete_inscripcion.html'
    success_url = '/inscripcion_finales_lista'

class deleteMesa(DeleteView):
    model = MesaFinal
    template_name ='registration/delete_mesa.html'
    success_url = '/mesas_lista'
         

class institutoView(CreateView):
    model = Instituto
    form_class = institutoForms

    def form_valid(self, form):
        form.save()
        Instituto = form.cleaned_data.get('nombre_instituto')
        email = form.cleaned_data.get('email_instituto')
      
        
        return redirect('/')
    

class carreraView(CreateView):
       
    model = Carrera
    form_class = carreraForm

    def form_valid(self, form):
        form.save()
        Carrera = form.cleaned_data.get('nombre_carrera')
        Resolucion = form.cleaned_data.get('num_resolucion')
      
        
        return redirect('/')

class listUser(ListView):
    model = Usuario
    usuario=Usuario.objects.all()
    template_name = 'registration/list_user.html'
    
class listInscripcion(ListView):
    model = InscripcionFinal
    template_name = 'registration/list_inscripcion.html'

class listMesa(ListView):
    model = MesaFinal
    template_name = 'registration/mesas_finales_lista.html'
   
   
class showUser(ListView):
    model = Usuario
    template_name = 'registration/show_user.html'


def lista_materias_user(request):
    
    materias_disponibles = Materia.objects.all() 
    return render(request, 'materias/lista_materias_user.html', {'materias': materias_disponibles})

def lista_materias_admin(request):
    carreras = Carrera.objects.all()  
    materias_all = Materia.objects.all()
    query_carrera = request.GET.get('carrera')
    
    if query_carrera:
        
        materias_all = materias_all.filter(carrera__nombre_carrera__icontains=query_carrera)

    paginator = Paginator(materias_all, 10)
    page = request.GET.get('page')
    try:
        materias = paginator.page(page)
    except PageNotAnInteger:
        materias = paginator.page(1)
    except EmptyPage:
        materias = paginator.page(paginator.num_pages)
    
    return render(request, 'materias/lista_materias_admin.html', {'materias': materias, 'carreras': carreras})    
    

def alta_materia(request):
    previous_page = request.GET.get('previous', None)  # Obtener el parámetro 'previous' de la URL

    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exito_alta_materia')
        if previous_page == 'lista_materias_admin':  # Redirigir al listado de materias si venía desde allí
                return redirect('lista_materias_admin')  
    else:
        form = MateriaForm()
        print(form)
    return render(request, 'materias/alta_materia.html', {'form': form})


def exito_cambios_materia(request):
    return render(request, 'materias/exito_cambios_materia.html')

def exito_alta_materia(request):
    return render(request, 'materias/exito_alta_materia.html')
def alerta_materia_existente(request):
    return render(request, 'alerta_materia_existente')


def inscribirse_materia(request, materia_id):
    materia = Materia.objects.get(pk=materia_id)

    if inscripcion.objects.filter(estudiante=request.user, materia=materia).exists():
        return redirect('lista_materias')
    inscripciones_materia = inscripcion.objects.filter(materia=materia)
    if inscripciones_materia.count() >= materia.cupo:
        return redirect ('lista_materias')

    usuarios_materia = usuarios_materia(materia=materia,usuario=request.user,modalidad='Regular')
    usuarios_materia.save()
    inscripcion = inscripcion(estudiante=request.user, materia=materia)
    inscripcion.save()

    return redirect('lista_materias')

def listarMateriasFinal(request):
    materias_final = []
    materias_disponibles=usuarios_materia.objects.filter(request.user,aprobada=False)
    for m in materias_disponibles:
        if m.puede_inscribirse_en_mesa_final() and MesaFinal.objects.filter(materia=m.materia,vigente=True).exisist():
            for mf in MesaFinal.objects.filter(materia=m.materia,vigente=True):
                materias_final.append(mf)
    return render(request, 'listarMateriasFinal.html', {'materias_final' : materias_final})

def altaMesa(request):
    if request.method == 'POST':
        form = MesaFinalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_mesa')  # Redirige a la lista de mesas finales
    else:
        form = MesaFinalForm()
    return render(request, 'finales/alta_mesa_final.html', {'form': form})

def inscripcionMesa(request):
    if request.method == 'POST':
        form = InscripcionFinalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exito_inscripcion_final')  # Redirige a la página de éxito de inscripción
    else:
        form = InscripcionFinalForm()
    return render(request, 'finales/inscripcion_final.html', {'form': form})

def exito_inscripcion_final(request):
    return render(request, 'finales/exito_inscripcion_final.html')

################################################################
def inscripcionFinal(request):
    if request.method == 'POST':
        final_usuario=request.POST['usuario']
        final_llamado=request.POST['llamado']
        form = InscripcionFinalForm(request.POST)
        if form.is_valid():
            if InscripcionFinal.objects.filter(usuario=final_usuario, llamado=final_llamado).count()<1:
                form.save()
                return redirect('exito_inscripcion_mesa')  # Redirige a pagina de exito de alta de mesa
            else:
                return redirect('error_inscripcion_adm')             
    else:
        form = InscripcionFinalForm()
    return render(request, 'finales/inscripcion_final_adm.html',  {'form': form}) 

def inscripcionFinal_est(request):
    if request.method == 'POST':
        final_usuario=request.POST['usuario']
        final_llamado=request.POST['llamado']
        form = InscripcionFinalForm(request.POST)
        if form.is_valid():
            if InscripcionFinal.objects.filter(usuario=final_usuario, llamado=final_llamado).count()<1:
                form.save()
                return redirect('exito_inscripcion_mesa')  # Redirige a pagina de exito de alta de mesa
            else:
                return redirect('error_inscripcion_est')             
    else:
        form = InscripcionFinalForm()
    
    return render(request, 'finales/inscripcion_final_est.html',  {'form': form})

def exito_inscripcion_mesa(request):
    return render(request, 'finales/exito_inscripcion_mesa.html')

def error_alta_mesa(request):
    return render(request, 'finales/error_alta_mesa.html')

def exito_alta_mesa(request):
    return render(request, 'finales/exito_alta_mesa.html')

def error_inscripcion_adm(request):
    return render(request, 'finales/error_inscripcion_adm.html')

def error_inscripcion_est(request):
    return render(request, 'finales/error_inscripcion_est.html')
    
################################################################
    

def crear_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EstudianteForm()
    return render(request, 'crear_estudiante.html', {'form':form})

def crear_profesor(request):
    if request.method =='POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ProfesorForm()
        return render(request, 'crear_profesor.html', {'form':form})
    

def crear_preceptor(request):
    if request.method =='POST':
        form = PreceptorForm(request.Post)
        if form.is_valid():
            form.save()
    else:
        form = PreceptorForm()
        return render(request, 'crear_preceptor.html',{'form':form})
    

def crear_Directivo(request):
    if request.method =='POST':
        form = DirectivoForm(request.Post)
        if form.is_valid():
            form.save()
    else:
        form = DirectivoForm()
        return render(request, 'crear_directivo.html',{'form':form})
    
    
class EstudianteCreateView(CreateView):
    model = Estudiante
    fields = ['username', 'password', 'matricula', ]
    template_name = 'estudiante_form.html'
    success_url = reverse_lazy('estudiante_lista')

class EstudianteUpdateView(UpdateView):
    model = Estudiante
    fields = ['username', 'matricula',]
    template_name = 'estudiante.form.html'
    success_url = reverse_lazy('estudiante_lista')

class EstudianteDeleteView(DeleteView):
    model = Estudiante
    template_name = 'confirmar_eliminar_estudiante.html'
    success_url = reverse_lazy('estudiante_lista')
    


def cargar_usuarios(request):
    if request.method == 'POST':
        formulario = ArchivoForm(request.POST, request.FILES)
        if formulario.is_valid():
            archivo_csv = request.FILES['csv_file']
            decoded_file = archivo_csv.read().decode('latin1').splitlines()
            archivo_csv = csv.DictReader(decoded_file,delimiter=';')
            flagDuplicado=0
            for fila in archivo_csv:
                try:
                    email = fila['Correo electrónico']
                    nombre_completo = fila['Nombre estudiante']
                    dni = fila['Documento estudiante']
                    username = dni
                    password = dni
                    matricula = dni
                    usuario = Estudiante.objects.create_user(email=email,nombre_completo=nombre_completo,rol='Estudiante', dni=dni,username=username, password=password, matricula=matricula)                
                except:
                    pass
                    flagDuplicado=1
            if flagDuplicado==0:
                return render(request,'registration/exito_carga_masiva.html')
            else:
                return render(request,'registration/warning_carga_masiva.html')
    else:
        formulario = ArchivoForm()

    return render(request, 'registration/cargar_usuarios.html', {'formulario': formulario})

def alta_masiva_materia(request):
    if request.method == 'POST' and request.Files['archivo_csv']:
        archivo_csv = request.FILES['archivo_csv']
        decoded_file = archivo_csv.read().decode('utf-8').splitlines() 
        archivo_csv= csv.DictReader(decoded_file) 

        for fila in archivo_csv:
            nombre = fila['nombre']
            profesor = fila['profesor']
            carrera = fila ['carrera']
        return HttpResponse ('Materias importadas correctamente')
    return render(request, 'alta_masiva_materia.html') 
    
def editar_materia(request, id):
    materia = get_object_or_404(Materia, id=id)
    if request.method == 'POST':
        form = MateriaForm(request.POST, instance=materia)
        if form.is_valid():
            form.save()
            return redirect('exito_cambios_materia')
    else:
        form = MateriaForm(instance=materia)
        return render(request, 'materias/editar_materia.html', {'form': form})


    
def eliminar_materia(request, id):
    materia = get_object_or_404(Materia, pk=id)
    if request.method == 'POST':
        materia.delete()
        return redirect('exito_materia_eliminada')
    return render(request, 'materias/eliminar_materia.html', {'materia': materia})



def eliminar_materias_seleccionadas(request):
    if request.method == 'POST':
        materia_ids = request.POST.getlist('materia_ids')
        if materia_ids:
            Materia.objects.filter(id__in=materia_ids).delete()
            return redirect('exito_materia_eliminada')
    return redirect('lista_materias_admin')

def exito_materia_eliminada(request):
    return render(request, 'materias/exito_materia_eliminada.html')

def ver_materias(request, id):
    materia = get_object_or_404(Materia, pk=id)
    return render(request, 'materias/ver_materia.html', {'materia': materia})

def cambiar_contraseña (request):
    if request.method == 'POST':
        
        username = User.objects.get(username='username')
        
        contraseña_nueva = request.POST['contraseña_nueva']
        
        username.set_password(contraseña_nueva)
        
        username.save()
        
        return HttpResponse('Su contraseña se cambio con exito')
    else : 
        return render(request, 'registration/change_password.html')  
    
  
def alta_estudiante(request):
        if request.method == 'POST' :
            form = EstudianteForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect (request, 'alta_exitosa.html')
        else:
            form = EstudianteForm()
            return render(request, 'alta_estudiante.html', {'form': form})
        
class MesasFinalesListView(ListView):
    model = MesaFinal
    template_name = 'finales/mesas_finales_list.html'
    context_object_name = 'mesas_finales'

def inscribir_mesa_final(request):
    if request.method == 'POST':
        filtro_form = FiltroInscripcionForm(request.POST)
        if filtro_form.is_valid():
            estudiante = filtro_form.cleaned_data.get('estudiante')
            materia = filtro_form.cleaned_data.get('materia')
            # Agrega lógica para filtrar según estudiante y/o materia
            mesas_finales = MesaFinal.objects.filter(materia__nombre__icontains=materia,
                                                      inscripcionfinal__usuario__nombre__icontains=estudiante)
        else:
            mesas_finales = MesaFinal.objects.all()
    else:
        filtro_form = FiltroInscripcionForm()
        mesas_finales = MesaFinal.objects.all()

    context = {'mesas_finales': mesas_finales, 'filtro_form': filtro_form}
    return render(request, 'finales/inscribir_mesa_final.html', context)

def listar_usuarios_materia(request):
    usuarios_materia_data = usuarios_materia.objects.all()  # Recupera todos los registros de usuarios_materia
    context = {'usuarios_materia_data': usuarios_materia_data}
    return render(request, 'registration/ver_usuarios_materia.html', context)


    