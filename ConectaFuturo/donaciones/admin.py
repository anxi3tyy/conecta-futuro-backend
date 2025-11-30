from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Donacion, Equipo, Entrega

class EquipoInline(admin.TabularInline):
    """Permite gestionar equipos directamente dentro de la ficha de Donación."""
    model = Equipo
    extra = 1  
    fields = ('tipo_equipo', 'estado', 'fecha_ingreso')
    readonly_fields = ('fecha_ingreso',)

@admin.register(Donacion)
class DonacionAdmin(admin.ModelAdmin):
    """Administración de las Donaciones."""
    list_display = ('id', 'tipo', 'donante', 'cantidad', 'fecha')
    list_filter = ('fecha', 'tipo')
    search_fields = ('tipo', 'descripcion', 'donante__username', 'donante__email')

    inlines = [EquipoInline]
    
    fieldsets = (
        ('Detalles del Aporte', {
            'fields': ('donante', 'tipo', 'cantidad', 'descripcion')
        }),
        ('Auditoría', {
            'fields': ('fecha',),
            'classes': ('collapse',),
        }),
    )
   
    autocomplete_fields = ['donante'] 
    readonly_fields = ('fecha',)
    date_hierarchy = 'fecha'
    ordering = ('-fecha',)

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    """Inventario de equipos físicos."""
    list_display = ('id', 'tipo_equipo', 'estado', 'donacion_link', 'fecha_ingreso')
    list_filter = ('estado', 'tipo_equipo')
    search_fields = ('tipo_equipo', 'donacion__tipo')
    

    def donacion_link(self, obj):
        if obj.donacion:
            url = reverse("admin:donaciones_donacion_change", args=[obj.donacion.id])
            return format_html('<a href="{}">Ver Donación #{}</a>', url, obj.donacion.id)
        return "-"
    donacion_link.short_description = "Origen (Donación)"

    autocomplete_fields = ['donacion']

@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    """Registro de entregas a beneficiarios."""
    list_display = ('id', 'equipo', 'beneficiario', 'voluntario_username', 'fecha_entrega')
    list_filter = ('fecha_entrega',)
    search_fields = ('equipo__tipo_equipo', 'beneficiario__usuario__username')
    
    autocomplete_fields = ['equipo', 'beneficiario', 'voluntario']

    def voluntario_username(self, obj):
        if obj.voluntario and obj.voluntario.usuario:
            return obj.voluntario.usuario.username
        return "N/A"
    voluntario_username.short_description = 'Voluntario Responsable'