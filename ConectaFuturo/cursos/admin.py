from django.contrib import admin
from .models import Curso, Inscripcion

# Gestión de cursos
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre_curso', 'modalidad', 'duracion')
    list_filter = ('modalidad',)
    search_fields = ('nombre_curso', 'descripcion')

# Gestión de alumnos inscritos
@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('id_curso', 'id_beneficiario', 'fecha_inscripcion')
    list_filter = ('fecha_inscripcion', 'id_curso')
    search_fields = ('id_beneficiario__username', 'id_curso__nombre_curso')