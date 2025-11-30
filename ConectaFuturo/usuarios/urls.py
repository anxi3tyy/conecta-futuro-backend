from django.urls import path
from . import views


urlpatterns = [
    #acceso y registro
    path('mi-panel/', views.redireccion_usuarios, name='dashboard_redirect'),
    path('registro/', views.registro_view, name='registro_usuario'),
    path('logout/', views.logout_usuario, name='logout_usuario'),
    
    #dashboards
    path('dashboard/beneficiario/', views.dashboard_beneficiario, name='dashboard_beneficiario'),
    path('dashboard/instructor/', views.dashboard_instructor, name='dashboard_instructor'),
    path('dashboard/donante/', views.dashboard_donante, name='dashboard_donante'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    
    #servicio tecnico
    path('dashboard/servicio/', views.dashboard_servicio, name='dashboard_servicio'), 
    path('servicio/crear/', views.servicio_crear_solicitud, name='servicio_crear'), 
    
    # Gestión de Tickets
    path('servicio/editar/<int:solicitud_id>/', views.servicio_editar_solicitud, name='servicio_editar'),
    path('servicio/estado/<int:solicitud_id>/', views.servicio_cambiar_estado_rapido, name='servicio_cambiar_estado'), 
    path('servicio/eliminar/<int:solicitud_id>/', views.servicio_eliminar_solicitud, name='servicio_eliminar'),
    
    #administrador
    path('admin/eliminar/usuario/<int:usuario_id>/', views.admin_eliminar_usuario, name='admin_eliminar_usuario'),
    path('admin/eliminar/curso/<int:curso_id>/', views.admin_eliminar_curso, name='admin_eliminar_curso'),
    path('admin/eliminar/donacion/<int:donacion_id>/', views.admin_eliminar_donacion, name='admin_eliminar_donacion'),
    
    # Editar
    path('admin/editar/usuario/<int:usuario_id>/', views.admin_editar_usuario, name='admin_editar_usuario'),
    path('admin/editar/curso/<int:curso_id>/', views.admin_editar_curso, name='admin_editar_curso'),
    path('admin/editar/donacion/<int:donacion_id>/', views.admin_editar_donacion, name='admin_editar_donacion'),

    #publico
    path('contacto/servicio/', views.contacto_servicio_view, name='contacto_servicio'),
]