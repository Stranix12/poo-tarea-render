from django.shortcuts import render, get_object_or_404, redirect
from .models import Cargo, Empleado
from .forms import CargoForm, EmpleadoForm
from django.db.models.deletion import ProtectedError
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

def inicio(request):
    return render(request, 'empleados/inicio.html')

def cargo_eliminar(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    empleados_asociados = cargo.empleado_set.all()
    if request.method == 'POST':
        try:
            cargo.delete()
            return redirect('cargo_listar')
        except ProtectedError:
            return render(request, 'empleados/cargos/confirmar_eliminar.html', {
                'cargo': cargo,
                'error': f'No se puede eliminar "{cargo.nombre}" porque tiene empleados asignados.',
                'empleados_asociados': empleados_asociados,
            })
    return render(request, 'empleados/cargos/confirmar_eliminar.html', {
        'cargo': cargo,
        'empleados_asociados': empleados_asociados,
    })

def cargo_listar(request):
    cargos = Cargo.objects.all()
    return render(request, 'empleados/cargos/listar.html', {'cargos': cargos})

def cargo_crear(request):
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cargo_listar')
    else:
        form = CargoForm()
    return render(request, 'empleados/cargos/formulario.html', {'form': form})

def cargo_editar(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            return redirect('cargo_listar')
    else:
        form = CargoForm(instance=cargo)
    return render(request, 'empleados/cargos/formulario.html', {'form': form})

# ==================== EMPLEADOS ====================

def empleado_listar(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados/empleados/listar.html', {'empleados': empleados})

def empleado_crear(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('empleado_listar')
    else:
        form = EmpleadoForm()
    return render(request, 'empleados/empleados/formulario.html', {'form': form})

def empleado_editar(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('empleado_listar')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'empleados/empleados/formulario.html', {'form': form})

def empleado_eliminar(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('empleado_listar')
    return render(request, 'empleados/empleados/confirmar_eliminar.html', {'empleado': empleado})

# ==================== CARGOS VBC ====================

class CargoListView(ListView):
    model = Cargo
    template_name = 'empleados/cargos/listar.html'
    context_object_name = 'cargos'

class CargoCreateView(CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'empleados/cargos/formulario.html'
    success_url = reverse_lazy('vbc_cargo_listar')

class CargoUpdateView(UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'empleados/cargos/formulario.html'
    success_url = reverse_lazy('vbc_cargo_listar')

class CargoDeleteView(DeleteView):
    model = Cargo
    template_name = 'empleados/cargos/confirmar_eliminar.html'
    success_url = reverse_lazy('vbc_cargo_listar')

# ==================== EMPLEADOS VBC ====================

class EmpleadoListView(ListView):
    model = Empleado
    template_name = 'empleados/empleados/listar.html'
    context_object_name = 'empleados'

class EmpleadoCreateView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleados/empleados/formulario.html'
    success_url = reverse_lazy('vbc_empleado_listar')

class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleados/empleados/formulario.html'
    success_url = reverse_lazy('vbc_empleado_listar')

class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'empleados/empleados/confirmar_eliminar.html'
    success_url = reverse_lazy('vbc_empleado_listar')

# Create your views here.
