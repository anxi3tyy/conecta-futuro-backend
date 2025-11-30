from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.forms import modelform_factory
from .models import Usuario, Beneficiario, Donante, Instructor, Servicio, Voluntario, SolicitudServicio
from cursos.models import Curso, Inscripcion
from donaciones.models import Donacion
from .forms import RegistroUsuarioForm, SolicitudServicioForm, GestionSolicitudForm, SolicitudInternaForm
from cursos.forms import CursoForm
from donaciones.forms import DonacionForm

#acceso

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    return render(request, 'index.html')

@login_required
def redireccion_usuarios(request):
    user = request.user
    tipo = str(user.tipo_usuario).strip().lower() if user.tipo_usuario else 'sin_rol'

    if tipo == 'beneficiario': return redirect('dashboard_beneficiario')
    elif tipo == 'instructor': return redirect('dashboard_instructor')
    elif tipo == 'donante': return redirect('dashboard_donante')
    elif tipo in ['servicio', 'voluntario']: return redirect('dashboard_servicio')
    elif tipo == 'admin' or user.is_superuser: return redirect('dashboard_admin')
    else:
        messages.warning(request, f'Rol "{tipo}" no reconocido.')
        logout(request)
        return redirect('home')

def registro_view(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                if user.tipo_usuario == 'beneficiario': Beneficiario.objects.create(usuario=user)
                elif user.tipo_usuario == 'instructor': Instructor.objects.create(usuario=user)
                elif user.tipo_usuario == 'donante': Donante.objects.create(usuario=user)
                elif user.tipo_usuario == 'servicio': Servicio.objects.create(usuario=user)
                elif user.tipo_usuario == 'voluntario': Voluntario.objects.create(usuario=user)
            except: pass
            
            messages.success(request, 'Registro exitoso.')
            if request.user.is_authenticated and request.user.is_superuser:
                return redirect('dashboard_admin')
            return redirect('login_usuario')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def logout_usuario(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Sesión cerrada.")
    return redirect('home')

#dashboards

@login_required
def dashboard_beneficiario(request):
    cursos = Curso.objects.all()
    for c in cursos:
        c.inscrito = Inscripcion.objects.filter(id_beneficiario=request.user, id_curso=c).exists()
    return render(request, 'usuarios/display_beneficiario.html', {'usuario': request.user, 'cursos': cursos})

@login_required
def dashboard_instructor(request):
    return render(request, 'usuarios/display_instructor.html', {'usuario': request.user, 'cursos': Curso.objects.all()})

@login_required
def dashboard_donante(request):
    return render(request, 'usuarios/display_donante.html', {
        'usuario': request.user, 
        'donaciones': Donacion.objects.filter(donante=request.user).order_by('-fecha')
    })

#servicio tecnico

@login_required
def dashboard_servicio(request):

    if request.user.tipo_usuario not in ['servicio', 'voluntario', 'admin'] and not request.user.is_superuser:
        return redirect('home')

    mensajes_web = SolicitudServicio.objects.filter(estado='falta_ingreso').order_by('-fecha_solicitud')
    
    equipos_taller = SolicitudServicio.objects.exclude(estado='falta_ingreso').order_by('-fecha_solicitud')

    print(f"--- DASHBOARD SERVICIO ---")
    print(f"Mensajes Web encontrados: {mensajes_web.count()}")
    print(f"Equipos en Taller encontrados: {equipos_taller.count()}")

    context = {
        'usuario': request.user,
        'mensajes_web': mensajes_web,
        'equipos_taller': equipos_taller,
        'pendientes': equipos_taller.filter(estado='pendiente').count(),
        'en_proceso': equipos_taller.filter(estado='en_proceso').count()
    }
    return render(request, 'usuarios/display_servicio.html', context)

@login_required
def servicio_crear_solicitud(request):
    """Ingreso manual de equipo"""
    if request.user.tipo_usuario not in ['servicio', 'voluntario', 'admin'] and not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = SolicitudInternaForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.email_contacto = "presencial@taller.local"
            ticket.telefono_contacto = "Presencial"
            ticket.tecnico_asignado = request.user
            ticket.estado = 'pendiente'
            ticket.save()
            messages.success(request, f"Equipo '{ticket.equipo}' ingresado correctamente.")
            return redirect('dashboard_servicio')
    else:
        form = SolicitudInternaForm()
    
    return render(request, 'usuarios/servicio_crear_solicitud.html', {'form': form})

@login_required
def servicio_editar_solicitud(request, solicitud_id):
    """Edición completa"""
    solicitud = get_object_or_404(SolicitudServicio, id=solicitud_id)
    if request.method == 'POST':
        form = GestionSolicitudForm(request.POST, instance=solicitud)
        if form.is_valid():
            ticket = form.save(commit=False)
            if not ticket.tecnico_asignado: ticket.tecnico_asignado = request.user
            ticket.save()
            messages.success(request, f'Solicitud #{ticket.id} actualizada.')
            return redirect('dashboard_servicio')
    else:
        form = GestionSolicitudForm(instance=solicitud)
    return render(request, 'usuarios/editar_ticket.html', {'form': form, 'solicitud': solicitud})

@login_required
def servicio_cambiar_estado_rapido(request, solicitud_id):
    """Cambio rápido (Dropdown)"""
    if request.user.tipo_usuario not in ['servicio', 'voluntario', 'admin'] and not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        solicitud = get_object_or_404(SolicitudServicio, id=solicitud_id)
        nuevo_estado = request.POST.get('nuevo_estado')
        estados_validos = dict(SolicitudServicio.ESTADOS).keys()
        
        if nuevo_estado in estados_validos:
            solicitud.estado = nuevo_estado
            if not solicitud.tecnico_asignado:
                solicitud.tecnico_asignado = request.user
            solicitud.save()
            messages.success(request, f"Estado actualizado a: {solicitud.get_estado_display()}")
        else:
            messages.error(request, "Estado no válido.")
            
    return redirect('dashboard_servicio')

@login_required
def servicio_eliminar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudServicio, id=solicitud_id)
    solicitud.delete()
    messages.success(request, 'Registro eliminado.')
    return redirect('dashboard_servicio')

def contacto_servicio_view(request):
    """Formulario público de contacto"""
    if request.method == 'POST':
        form = SolicitudServicioForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.estado = 'falta_ingreso' 
            ticket.save()
            
            print(f"✅ CONTACTO RECIBIDO: {ticket.equipo} - Estado: {ticket.estado}")
            messages.success(request, "Solicitud enviada. Nos contactaremos pronto.")
            return redirect('home')
        else:
            print("❌ ERROR EN CONTACTO:")
            print(form.errors)
            messages.error(request, "Error al enviar la solicitud. Revisa los datos ingresados.")
    else:
        form = SolicitudServicioForm()
    return render(request, 'usuarios/contacto_servicio.html', {'form': form})

#administrador

def es_admin(user):
    return user.is_authenticated and (user.tipo_usuario == 'admin' or user.is_superuser)

@login_required
def dashboard_admin(request):
    if not es_admin(request.user): return redirect('home')

    context = {
        'usuario': request.user,
        'total_usuarios': Usuario.objects.count(),
        'total_cursos': Curso.objects.count(),
        'total_donaciones': Donacion.objects.count(),
        'lista_usuarios': Usuario.objects.all().order_by('-date_joined'),
        'lista_cursos': Curso.objects.all(),
        'lista_donaciones': Donacion.objects.all().order_by('-fecha'),
    }
    return render(request, 'usuarios/display_admin.html', context)

#eliminar
@login_required
def admin_eliminar_usuario(request, usuario_id):
    if not es_admin(request.user): return redirect('home')
    u = get_object_or_404(Usuario, id=usuario_id)
    if u != request.user: u.delete()
    return redirect('dashboard_admin')

@login_required
def admin_eliminar_curso(request, curso_id):
    if not es_admin(request.user): return redirect('home')
    get_object_or_404(Curso, id=curso_id).delete()
    return redirect('dashboard_admin')

@login_required
def admin_eliminar_donacion(request, donacion_id):
    if not es_admin(request.user): return redirect('home')
    get_object_or_404(Donacion, id=donacion_id).delete()
    return redirect('dashboard_admin')

#editar
@login_required
def admin_editar_usuario(request, usuario_id):
    if not es_admin(request.user): return redirect('home')
    obj = get_object_or_404(Usuario, id=usuario_id)
    FormClass = modelform_factory(Usuario, fields=('username', 'email', 'tipo_usuario', 'is_active'))
    
    if request.method == 'POST':
        form = FormClass(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard_admin')
    else:
        form = FormClass(instance=obj)
    return render(request, 'usuarios/admin_editar_form.html', {'form': form, 'titulo': f'Editar Usuario: {obj.username}'})

@login_required
def admin_editar_curso(request, curso_id):
    if not es_admin(request.user): return redirect('home')
    obj = get_object_or_404(Curso, id=curso_id)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard_admin')
    else:
        form = CursoForm(instance=obj)
    return render(request, 'usuarios/admin_editar_form.html', {'form': form, 'titulo': f'Editar Curso: {obj.nombre_curso}'})

@login_required
def admin_editar_donacion(request, donacion_id):
    if not es_admin(request.user): return redirect('home')
    obj = get_object_or_404(Donacion, id=donacion_id)
    if request.method == 'POST':
        form = DonacionForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard_admin')
    else:
        form = DonacionForm(instance=obj)
    return render(request, 'usuarios/admin_editar_form.html', {'form': form, 'titulo': 'Editar Donación'})