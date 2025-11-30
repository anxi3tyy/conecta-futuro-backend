from django.urls import path
from . import views

urlpatterns = [ 
    # instructor
    path('crear/', views.crear_curso, name='crear_curso'),
    path('editar/<int:curso_id>/', views.editar_curso, name='editar_curso'),       
    path('eliminar/<int:curso_id>/', views.eliminar_curso, name='eliminar_curso'), 
    
    # beneficiarios
    path('inscribir/<int:curso_id>/', views.inscribir_curso, name='inscribir_curso'),
    path('cancelar/<int:curso_id>/', views.cancelar_inscripcion, name='cancelar_inscripcion'),
    
    # publico
    path('', views.lista_cursos, name='lista_cursos'),
    
    # API Externa (Google Books)
    path('biblioteca/', views.biblioteca_digital, name='biblioteca_digital'),
    
    path('api/lista/', views.CursoListAPI.as_view(), name='curso_list_api'),
]