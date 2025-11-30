from django.db import models
from usuarios.models import Usuario

class Donacion(models.Model):
    donante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='donaciones')
    tipo = models.CharField(max_length=100, verbose_name="Tipo de Donación") 
    descripcion = models.TextField(verbose_name="Descripción")
    cantidad = models.PositiveIntegerField(default=1)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.donante.username}"

class Equipo(models.Model):
    tipo_equipo = models.CharField(max_length=50)
    estado = models.CharField(max_length=20)
    donacion = models.ForeignKey(Donacion, on_delete=models.SET_NULL, blank=True, null=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_equipo} ({self.estado})"

class Entrega(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    beneficiario = models.ForeignKey('usuarios.Beneficiario', on_delete=models.CASCADE)
    voluntario = models.ForeignKey('usuarios.Voluntario', on_delete=models.SET_NULL, null=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Entrega de {self.equipo} a {self.beneficiario}"