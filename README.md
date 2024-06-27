# Proyecto Gestión de Inscripciones a Final del **Instituto 210**

## Proyecto de articulación de materias de la Carrera Tecnicatura Superior en Analisís de Sistemas

## Instalación desde consola

Para descargar el proyecto se puede ejecutar:

`git clone git@gitlab.com:fsantolaria/gestionInstituto.git`

Antes de iniciar el proyecto de deberá copiar el archivo:

En Linux o desde Windows Powershell:
`cp settings_DEV.py settings.py`

En Windows CMD:
`copy settings_DEV.py settings.py`

Agregar 'inscripcionFinales', en INSTALLED_APPS dentro del archivo settings.py

Posteriormente ejecutar las migrations faltantes:

`python manage.py makemigrations`

`python manage.py migrate`

Para acceder al backoffice http://127.0.0.1:8000/admin se deberá crear un usuario superadmin de la forma:

`python manage.py createsuperuser`

Para ejecutar el proyecto se debe:

`python manage.py runserver`

Para acceder al login, ingresar a http://127.0.0.1:8000 desde el navegador.

Para redireccionar al index luego del login agregar en settings.py

`LOGIN_REDIRECT_URL = 'inicio'`
<!-- Fin -->
"# Instituto210Proyecto"
#prueba prueba
