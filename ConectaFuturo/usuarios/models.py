from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = (
        ('beneficiario', 'Beneficiario'),
        ('instructor', 'Instructor'),
        ('donante', 'Donante'),
        ('servicio', 'Servicio'),
        ('voluntario', 'Voluntario'),
        ('admin', 'Administrador'),
    )
    
    tipo_usuario = models.CharField(max_length=15, choices=TIPO_USUARIO_CHOICES)
    email = models.EmailField(unique=True, null=True, blank=True)

    REQUIRED_FIELDS = ['email', 'tipo_usuario']
    
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Beneficiario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    id_rsh = models.CharField(max_length=20, blank=True, null=True)
    tramo_rsh = models.CharField(max_length=20, blank=True, null=True)
    nivel_digital = models.CharField(max_length=20, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

class Instructor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)

class Donante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    tipo_donante = models.CharField(max_length=50, blank=True, null=True)

class Voluntario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)

class Servicio(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    cargo_servicio = models.CharField(max_length=100, blank=True, null=True)

class SolicitudServicio(models.Model):
    ESTADOS = (
        ('falta_ingreso', 'Falta Ingreso (Solicitud Web)'),
        
        ('pendiente', 'Pendiente de Revisión'),
        ('en_proceso', 'En Reparación/Diagnóstico'),
        ('espera_repuesto', 'En Espera de Repuestos'),
        ('finalizado', 'Finalizado / Listo'),
        ('entregado', 'Entregado al Cliente'),
    )

    nombre_contacto = models.CharField(max_length=100, verbose_name="Nombre del Cliente")
    email_contacto = models.EmailField(verbose_name="Email")
    telefono_contacto = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    
    equipo = models.CharField(max_length=100, verbose_name="Equipo")
    descripcion_problema = models.TextField(verbose_name="Problema Reportado")

    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default='falta_ingreso')
    
    tecnico_asignado = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='asignaciones_tecnicas')
    notas_tecnicas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.equipo} - {self.estado}"