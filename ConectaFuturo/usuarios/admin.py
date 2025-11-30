#para todos los admin.py me toco usar ia para generarlos(no termine de entender bien como funcionan)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Beneficiario, Donante, Instructor, Servicio, Voluntario, SolicitudServicio

class CustomUserAdmin(UserAdmin):
    model = Usuario

    list_display = ['username', 'email', 'tipo_usuario', 'is_staff', 'is_active']

    list_filter = ['tipo_usuario', 'is_staff', 'is_active']

    search_fields = ['username', 'email']
    

    fieldsets = UserAdmin.fieldsets + (
        ('Información de Rol', {'fields': ('tipo_usuario',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información de Rol', {'fields': ('tipo_usuario',)}),
    )

admin.site.register(Usuario, CustomUserAdmin)



@admin.register(Beneficiario)
class BeneficiarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nivel_digital', 'tramo_rsh')
    search_fields = ('usuario__username', 'usuario__email') 
    list_filter = ('nivel_digital',)

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'especialidad')
    search_fields = ('usuario__username', 'especialidad')

@admin.register(Donante)
class DonanteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_donante')
    list_filter = ('tipo_donante',)
    search_fields = ('usuario__username', 'usuario__email') 

@admin.register(Voluntario)
class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'especialidad')
    list_filter = ('especialidad',)

    search_fields = ('usuario__username', 'usuario__email', 'especialidad') 

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cargo_servicio')
    search_fields = ('usuario__username', 'cargo_servicio') 

@admin.register(SolicitudServicio)
class SolicitudServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipo', 'nombre_contacto', 'estado', 'tecnico_asignado', 'fecha_solicitud')
    list_filter = ('estado', 'fecha_solicitud')
    search_fields = ('equipo', 'nombre_contacto', 'email_contacto')

    list_editable = ('estado', 'tecnico_asignado') 
    date_hierarchy = 'fecha_solicitud'
    
    autocomplete_fields = ['tecnico_asignado']