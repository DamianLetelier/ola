from django.shortcuts import render, redirect, get_object_or_404
from crud_Matias.models import Empleado
from .forms import EmpleadoForm

def lista_empleado(request):
    empleados = Empleado.objects.all()
    return render(request, 'crud_Matias/lista.html', {'empleados': empleados})

def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'crud_Matias/formulario.html', {'form': form})

def actualizar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    form = EmpleadoForm(request.POST or None, instance=empleado)
    if form.is_valid():
        form.save()
        return redirect('lista_empleados')
    return render(request, 'crud_Matias/formulario.html', {'form': form})

def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('lista_empleados')
    return render(request, 'crud_Matias/eliminar.html', {'empleado': empleado})
