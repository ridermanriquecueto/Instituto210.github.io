import csv
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.forms import DateInput
from django.contrib.auth.forms import UserCreationForm
#from django.forms import ModelForm, CustomPasswordChangeForm
from .models import *
class institutoForms(forms.ModelForm):
      nombre_instituto = forms.CharField(max_length=30)
      email = forms.CharField(max_length=20)
      class Meta:
            model = Instituto
            fields = (
            'nombre_instituto',
            'email_instituto',
            'direccion',
            'localidad',
            'ciudad',
            )


class carreraForm(forms.ModelForm):
      nombre_carrera = forms.CharField( max_length=100)
      num_resolucion = forms.CharField(max_length=100)
      class Meta:
        model = Carrera
        fields =(
          'nombre_carrera',
          'num_resolucion',
          'duracion_carrera',
          'instituto',

        )

class usuarios_materiaForm(forms.ModelForm):
      nombre_materia = forms.CharField( max_length=100)
      class Meta:
        model = Materia
        fields =(
          'nombre_materia',
          'carrera',
          'profesor'

        )

class usuarios_materiaForm(forms.ModelForm):
      nombre_materia = forms.CharField( max_length=100)
      class Meta:
        model = Materia
        fields =(
          'nombre_materia',
          'carrera',
          'profesor'

        )

class materiaCorrelativaForm(forms.ModelForm):
      nombre_materiaCorrelativa = forms.CharField( max_length=100)
      class Meta:
        model = MateriaCorrelativa
        fields =(
          'materia',
          'materia_correlativa'
        )

class registri_user_form(UserCreationForm):
    email = forms.EmailField(required=True)
    dni = forms.IntegerField(max_value=8)   

    password1 = None
    password2 = None
    
    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.all(),
        empty_label="Seleccione una carrera"
    )
    especialidad = forms.CharField(max_length=100, required=False)
    cargo = forms.CharField(max_length=100, required=False)
    area = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Usuario
        fields = ['email', 'nombre_completo', 'dni', 'rol', 'carrera', 'especialidad', 'cargo', 'area']

    def clean(self):
        password = Usuario.objects.make_random_password(length=10,allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        self.cleaned_data['password1'] = password
        self.cleaned_data['password2'] = password

        return super().clean()

    def save(self, commit=True):
        usuario = super().save(commit=False)
        rol = self.cleaned_data.get('rol', '').lower()

        if rol == 'Estudiante':
            estudiante = Estudiante.objects.create(
                email=usuario.email,
                nombre_completo=usuario.nombre_completo,
                dni=usuario.dni,
                rol=usuario.rol,
            )
            estudiante.carrera.set([self.cleaned_data['carrera']])
            usuario = estudiante
        elif rol == 'Profesor':
            usuario = Profesor.objects.create(
                email=usuario.email,
                nombre_completo=usuario.nombre_completo,
                dni=usuario.dni,
                rol=usuario.rol,
                especialidad=self.cleaned_data['especialidad']
            )
        elif rol == 'Directivo':
            usuario = Directivo.objects.create(
                email=usuario.email,
                nombre_completo=usuario.nombre_completo,
                dni=usuario.dni,
                rol=usuario.rol,
                cargo=self.cleaned_data['cargo']
            )
        elif rol == 'Preceptor':
            usuario = Preceptor.objects.create(
                email=usuario.email,
                nombre_completo=usuario.nombre_completo,
                dni=usuario.dni,
                rol=usuario.rol,
                area=self.cleaned_data['area']
            )
               
        usuario.save()
        return usuario



class profile_students_form(forms.ModelForm):   
  class Meta:
    model = Usuario
    fields = (
      'username',
      'nombre_completo',
      'fecha_nac',
      'dni',
      'direccion',
      'localidad',
      'ciudad',
      'nacionalidad',
      'telefono_1',
      'telefono_2',
      'estado_civil',
      'sexo',
      

    )
    
class mesa_form(forms.ModelForm):   
  class Meta:
    model = MesaFinal
    fields = (
      'materia',
      'llamado'
    )
    
class edit_profile_form(forms.ModelForm):   
  class Meta:
    model = Usuario
    fields = (
      'username',
      'email',
      'nombre_completo',
      'fecha_nac',
      'dni',
      'direccion',
      'localidad',
      'ciudad',
      'nacionalidad',
      'telefono_1',
      'telefono_2',
      'estado_civil',
      'sexo',
      

    )

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = '__all__'

class ProfesorForm(forms.ModelForm):
    class Meta: 
        model = Profesor
        fields = '__all__' 

class PreceptorForm(forms.ModelForm):
    class Meta:
        model = Preceptor
        fields = '__all__'
class DirectivoForm(forms.ModelForm):
    class Meta:
        model = Directivo 
        fields = '__all__'


############################################################
class MateriaForm(forms.ModelForm):
      class Meta:
        model = Materia
        
        fields = ['nombre_materia', 'carrera', 'profesor', 'anio', 'dia', 'Horario']
        widgets = {
           'nombre_materia': forms.TextInput(attrs={'class':'form-control'}),
           'carrera': forms.Select(attrs={'class':'form-control'}),
           'profesor': forms.Select(attrs={'class':'form-control'}),
           'anio': forms.Select(attrs={'class':'form-control'}),
           'dia': forms.Select(attrs={'class':'form-control'}),
           'Horario': forms.Select(attrs={'class':'form-control'}),
        }
        labels = {
           'nombre_materia': 'Nombre materia',
           'carrera': 'Carrera',
           'profesor': 'Profesor',
           'anio': 'Año', 
           'dia' : 'Día',
           'horario' : 'Horario',
        }


class MesaFinalForm(forms.ModelForm):
    class Meta:
        model = MesaFinal
        fields = ['materia', 'llamado']
        widgets = {
            'llamado': DateInput(attrs={'type': 'date'}),
        }

class InscripcionFinalForm(forms.ModelForm):
    class Meta:
        model = InscripcionFinal
        fields = ['usuario', 'llamado']

# en tu aplicación (app) forms.py

class InscripcionFinalForm(forms.ModelForm):
    class Meta:
        model = InscripcionFinal
        fields = ['usuario', 'llamado', 'aprobada']

class FiltroInscripcionForm(forms.Form):
    estudiante = forms.CharField(required=False)
    materia = forms.CharField(required=False)
