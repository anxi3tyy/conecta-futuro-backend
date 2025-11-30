from django.db import models
from usuarios.models import Usuario

class Curso(models.Model):
    nombre_curso = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    duracion = models.IntegerField(blank=True, null=True)
    modalidad = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre_curso

class Inscripcion(models.Model):
    id_beneficiario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_beneficiario.username} inscrito en {self.id_curso.nombre_curso}"