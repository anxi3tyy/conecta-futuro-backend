from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from usuarios import views as usuarios_views 

urlpatterns = [
    #inicio
    path('', usuarios_views.home, name='home'),
    #login
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login_usuario'),

    path('usuarios/', include('usuarios.urls')),
    path('cursos/', include('cursos.urls')),
    path('donaciones/', include('donaciones.urls')),
    path('admin/', admin.site.urls),
]