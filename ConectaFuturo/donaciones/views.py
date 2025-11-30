from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DonacionForm
from .models import Donacion

@login_required
def realizar_donacion(request):
    """
    Vista para registrar una nueva donación.
    """
    if request.user.tipo_usuario not in ['donante', 'admin'] and not request.user.is_superuser:
        messages.warning(request, "Debes tener perfil de donante para realizar esta acción.")
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = DonacionForm(request.POST)
        if form.is_valid():
            donacion = form.save(commit=False)
            donacion.donante = request.user 
            donacion.save()
            
            messages.success(request, f'¡Gracias! Hemos registrado tu donación de "{donacion.tipo}".')
            return redirect('dashboard_donante')
        else:
            messages.error(request, "Hubo un error en el formulario. Revisa los datos.")
    else:
        form = DonacionForm()

    return render(request, 'donaciones/donacion_form.html', {'form': form})