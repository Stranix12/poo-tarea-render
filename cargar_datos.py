"""
Script para cargar datos de prueba en la BD
Ejecutar desde la terminal:
.\CRUD\Scripts\python.exe cargar_datos.py
"""

import os
import django
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocrud.settings')
django.setup()

from empleados.models import Cargo, Empleado

# Limpiar datos existentes
print("Limpiando datos existentes...")
Empleado.objects.all().delete()
Cargo.objects.all().delete()

# Crear cargos
print("\nCreando cargos...")
cargos_data = [
    {'nombre': 'Gerente General', 'descripcion': 'Máxima autoridad de la empresa'},
    {'nombre': 'Desarrollador Backend', 'descripcion': 'Programador Python/Django'},
    {'nombre': 'Desarrollador Frontend', 'descripcion': 'Programador JavaScript/React'},
    {'nombre': 'Contador', 'descripcion': 'Gestión de finanzas y contabilidad'},
    {'nombre': 'Diseñador Gráfico', 'descripcion': 'Diseño de interfaces y materiales'},
    {'nombre': 'Administrador de BD', 'descripcion': 'Gestión de bases de datos'},
    {'nombre': 'Analista de Sistemas', 'descripcion': 'Análisis e implementación de sistemas'},
    {'nombre': 'Especialista en Marketing', 'descripcion': 'Estrategias de marketing digital'},
]

cargos = {}
for cargo_data in cargos_data:
    cargo = Cargo.objects.create(**cargo_data)
    cargos[cargo_data['nombre']] = cargo
    print(f"✓ {cargo.nombre}")

# Crear empleados
print("\nCreando empleados...")
empleados_data = [
    # Gerentes
    {'nombres': 'Carlos', 'apellidos': 'González López', 'correo': 'carlos.gonzalez@company.com', 'sueldo': 8500.00, 'cargo': 'Gerente General', 'dias_atras': 730},
    {'nombres': 'María', 'apellidos': 'Rodríguez García', 'correo': 'maria.rodriguez@company.com', 'sueldo': 7200.00, 'cargo': 'Gerente General', 'dias_atras': 365},

    # Desarrolladores Backend
    {'nombres': 'Juan', 'apellidos': 'Pérez Martínez', 'correo': 'juan.perez@company.com', 'sueldo': 5500.00, 'cargo': 'Desarrollador Backend', 'dias_atras': 180},
    {'nombres': 'Diego', 'apellidos': 'Sánchez Ruiz', 'correo': 'diego.sanchez@company.com', 'sueldo': 5200.00, 'cargo': 'Desarrollador Backend', 'dias_atras': 150},
    {'nombres': 'Luis', 'apellidos': 'Hernández Flores', 'correo': 'luis.hernandez@company.com', 'sueldo': 4800.00, 'cargo': 'Desarrollador Backend', 'dias_atras': 90},
    {'nombres': 'Andrés', 'apellidos': 'López Vargas', 'correo': 'andres.lopez@company.com', 'sueldo': 5000.00, 'cargo': 'Desarrollador Backend', 'dias_atras': 60},

    # Desarrolladores Frontend
    {'nombres': 'Ana', 'apellidos': 'Gutiérrez Moreno', 'correo': 'ana.gutierrez@company.com', 'sueldo': 5300.00, 'cargo': 'Desarrollador Frontend', 'dias_atras': 200},
    {'nombres': 'Laura', 'apellidos': 'Jiménez Castro', 'correo': 'laura.jimenez@company.com', 'sueldo': 4900.00, 'cargo': 'Desarrollador Frontend', 'dias_atras': 120},
    {'nombres': 'Sofía', 'apellidos': 'Martínez Ramos', 'correo': 'sofia.martinez@company.com', 'sueldo': 5100.00, 'cargo': 'Desarrollador Frontend', 'dias_atras': 80},

    # Contadores
    {'nombres': 'Roberto', 'apellidos': 'Gómez Ponce', 'correo': 'roberto.gomez@company.com', 'sueldo': 4200.00, 'cargo': 'Contador', 'dias_atras': 500},
    {'nombres': 'Patricia', 'apellidos': 'Acosta Silva', 'correo': 'patricia.acosta@company.com', 'sueldo': 3900.00, 'cargo': 'Contador', 'dias_atras': 250},

    # Diseñadores
    {'nombres': 'Ricardo', 'apellidos': 'Delgado Romero', 'correo': 'ricardo.delgado@company.com', 'sueldo': 4500.00, 'cargo': 'Diseñador Gráfico', 'dias_atras': 300},
    {'nombres': 'Valentina', 'apellidos': 'Ortega Santos', 'correo': 'valentina.ortega@company.com', 'sueldo': 4400.00, 'cargo': 'Diseñador Gráfico', 'dias_atras': 220},

    # Administrador de BD
    {'nombres': 'Miguel', 'apellidos': 'Navarro Vega', 'correo': 'miguel.navarro@company.com', 'sueldo': 5800.00, 'cargo': 'Administrador de BD', 'dias_atras': 400},

    # Analista
    {'nombres': 'Gabriela', 'apellidos': 'Vargas López', 'correo': 'gabriela.vargas@company.com', 'sueldo': 5400.00, 'cargo': 'Analista de Sistemas', 'dias_atras': 280},

    # Especialista en Marketing
    {'nombres': 'Fernando', 'apellidos': 'Blanco Morales', 'correo': 'fernando.blanco@company.com', 'sueldo': 4700.00, 'cargo': 'Especialista en Marketing', 'dias_atras': 350},
]

for emp_data in empleados_data:
    cargo_nombre = emp_data.pop('cargo')
    dias_atras = emp_data.pop('dias_atras')
    fecha_ingreso = (datetime.now() - timedelta(days=dias_atras)).date()

    empleado = Empleado.objects.create(
        **emp_data,
        cargo=cargos[cargo_nombre],
        fecha_ingreso=fecha_ingreso
    )
    print(f"✓ {empleado.nombres} {empleado.apellidos} - {cargo_nombre}")

print("\n" + "="*60)
print("✅ Datos cargados exitosamente!")
print("="*60)

# Mostrar resumen
print(f"\nResumen:")
print(f"- Total cargos: {Cargo.objects.count()}")
print(f"- Total empleados: {Empleado.objects.count()}")
print(f"- Sueldo máximo: ${Empleado.objects.latest('sueldo').sueldo:.2f}")
print(f"- Sueldo mínimo: ${Empleado.objects.earliest('sueldo').sueldo:.2f}")

from django.db.models import Avg
promedio = Empleado.objects.aggregate(Avg('sueldo'))['sueldo__avg']
print(f"- Sueldo promedio: ${promedio:.2f}")
