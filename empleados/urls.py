from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    # Cargos
    path('cargos/', views.cargo_listar, name='cargo_listar'),
    path('cargos/crear/', views.cargo_crear, name='cargo_crear'),
    path('cargos/editar/<int:pk>/', views.cargo_editar, name='cargo_editar'),
    path('cargos/eliminar/<int:pk>/', views.cargo_eliminar, name='cargo_eliminar'),

    # Empleados (vistas pendientes - se completarán después)
    path('empleados/', views.empleado_listar, name='empleado_listar'),
    path('empleados/crear/', views.empleado_crear, name='empleado_crear'),
    path('empleados/editar/<int:pk>/', views.empleado_editar, name='empleado_editar'),
    path('empleados/eliminar/<int:pk>/', views.empleado_eliminar, name='empleado_eliminar'),

        # Cargos VBC
    path('vbc/cargos/', views.CargoListView.as_view(), name='vbc_cargo_listar'),
    path('vbc/cargos/crear/', views.CargoCreateView.as_view(), name='vbc_cargo_crear'),
    path('vbc/cargos/editar/<int:pk>/', views.CargoUpdateView.as_view(), name='vbc_cargo_editar'),
    path('vbc/cargos/eliminar/<int:pk>/', views.CargoDeleteView.as_view(), name='vbc_cargo_eliminar'),

    # Empleados VBC
    path('vbc/empleados/', views.EmpleadoListView.as_view(), name='vbc_empleado_listar'),
    path('vbc/empleados/crear/', views.EmpleadoCreateView.as_view(), name='vbc_empleado_crear'),
    path('vbc/empleados/editar/<int:pk>/', views.EmpleadoUpdateView.as_view(), name='vbc_empleado_editar'),
    path('vbc/empleados/eliminar/<int:pk>/', views.EmpleadoDeleteView.as_view(), name='vbc_empleado_eliminar'),

]
