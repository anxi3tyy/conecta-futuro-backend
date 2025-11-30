from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Curso, Inscripcion
from .forms import CursoForm
import requests 
from rest_framework import generics
from .serializers import CursoSerializer

# Crear, editar y eliminar cursos

@login_required
def crear_curso(request):
    """Crear un nuevo curso."""
    if request.user.tipo_usuario not in ['instructor', 'admin'] and not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save()
            messages.success(request, f'¡Curso "{curso.nombre_curso}" creado exitosamente!')
            return redirect('dashboard_instructor')
    else:
        form = CursoForm()

    return render(request, 'cursos/crear_curso.html', {'form': form, 'titulo': 'Crear Nuevo Curso'})

@login_required
def editar_curso(request, curso_id):
    """Editar un curso existente."""
    # Seguridad básica
    if request.user.tipo_usuario not in ['instructor', 'admin'] and not request.user.is_superuser:
        return redirect('home')
        
    curso = get_object_or_404(Curso, id=curso_id)

    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, f'Curso "{curso.nombre_curso}" actualizado correctamente.')
            return redirect('dashboard_instructor')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'cursos/crear_curso.html', {'form': form, 'titulo': f'Editar Curso: {curso.nombre_curso}'})

@login_required
def eliminar_curso(request, curso_id):
    """Eliminar un curso."""
    if request.user.tipo_usuario not in ['instructor', 'admin'] and not request.user.is_superuser:
        return redirect('home')
        
    curso = get_object_or_404(Curso, id=curso_id)
    nombre = curso.nombre_curso
    curso.delete()
    messages.success(request, f'El curso "{nombre}" ha sido eliminado.')
    return redirect('dashboard_instructor')

#inscripcion beneficiarios
@login_required
def inscribir_curso(request, curso_id):
    if request.method != 'POST': return redirect('dashboard_beneficiario')
    curso = get_object_or_404(Curso, id=curso_id)
    inscripcion, created = Inscripcion.objects.get_or_create(id_beneficiario=request.user, id_curso=curso)
    if created: messages.success(request, 'Inscripción exitosa.')
    else: messages.info(request, 'Ya estabas inscrito.')
    return redirect('dashboard_beneficiario')

@login_required
def cancelar_inscripcion(request, curso_id):
    if request.method != 'POST': return redirect('dashboard_beneficiario')
    Inscripcion.objects.filter(id_beneficiario=request.user, id_curso__id=curso_id).delete()
    messages.warning(request, 'Inscripción cancelada.')
    return redirect('dashboard_beneficiario')

def lista_cursos(request):
    cursos = Curso.objects.all()
    libros_recomendados = []
    return render(request, 'cursos/lista_cursos.html', {'cursos': cursos, 'libros': libros_recomendados})

def biblioteca_digital(request):
    return render(request, 'cursos/biblioteca.html', {'libros': [], 'busqueda': ''})

class CursoListAPI(generics.ListAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer