# Lección completa: ORM Django

**Objetivo:** Aprender a interactuar con la base de datos usando Django ORM sin escribir SQL directo.

---

## Índice

1. [Nivel 1: Conceptos Básicos](#nivel-1-conceptos-básicos)
2. [Nivel 2: CRUD Básico](#nivel-2-crud-básico)
3. [Nivel 3: Querysets](#nivel-3-querysets)
4. [Nivel 4: Relaciones](#nivel-4-relaciones)
5. [Nivel 5: Agregaciones y Anotaciones](#nivel-5-agregaciones-y-anotaciones)
6. [Nivel 6: Optimización](#nivel-6-optimización)
7. [Ejercicios Prácticos](#ejercicios-prácticos)

---

## Nivel 1: Conceptos Básicos

### ¿Qué es un ORM?

**ORM** = Object-Relational Mapping

Convierte objetos Python en filas de base de datos y viceversa.

**Sin ORM (SQL directo):**
```sql
SELECT * FROM empleados_cargo WHERE nombre = 'Gerente';
```

**Con Django ORM:**
```python
Cargo.objects.filter(nombre='Gerente')
```

### El modelo

Un modelo Django es una **clase Python** que representa una **tabla de la BD**.

```python
class Cargo(models.Model):  # Tabla "empleados_cargo"
    nombre = models.CharField(max_length=100)  # Columna "nombre"
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre
```

**Equivalente en BD:**
```
Tabla: empleados_cargo
├── id (PK, auto)
├── nombre (VARCHAR 100)
└── descripcion (VARCHAR 200, nullable)
```

### Conceptos clave

| Concepto | Qué es | Ejemplo |
|---|---|---|
| **Model** | Clase que representa una tabla | `class Cargo(models.Model)` |
| **Field** | Columna de la tabla | `nombre = models.CharField()` |
| **Instance** | Un objeto de un modelo (una fila) | `cargo = Cargo(nombre='Gerente')` |
| **QuerySet** | Conjunto de objetos de la BD | `Cargo.objects.all()` |
| **Manager** | Interfaz para consultar | `Cargo.objects` |

---

## Nivel 2: CRUD Básico

### C — CREATE (Crear registros)

**Forma 1: Instanciar y guardar**
```python
cargo = Cargo(nombre='Gerente', descripcion='Líder de equipo')
cargo.save()
```

**Forma 2: Crear directamente**
```python
cargo = Cargo.objects.create(
    nombre='Desarrollador',
    descripcion='Programador backend'
)
```

**Diferencia:**
- `Cargo(...)` — crea el objeto en memoria, no en la BD
- `.save()` — lo guarda en la BD
- `.create()` — hace ambas cosas en una línea

**Con valores relacionados (FK):**
```python
cargo = Cargo.objects.get(nombre='Gerente')
empleado = Empleado.objects.create(
    nombres='Juan',
    apellidos='Pérez',
    correo='juan@example.com',
    sueldo=3000.00,
    fecha_ingreso='2024-01-15',
    cargo=cargo  # Asignar el objeto Cargo
)
```

---

### R — READ (Leer datos)

**Obtener todos los registros:**
```python
cargos = Cargo.objects.all()
# RetornaQuerySet: <QuerySet [<Cargo: Gerente>, <Cargo: Desarrollador>]>
```

**Obtener uno por condición:**
```python
cargo = Cargo.objects.get(nombre='Gerente')
# Retorna un objeto Cargo
# ❌ EXCEPCIONES:
# - Si no existe: DoesNotExist
# - Si hay múltiples: MultipleObjectsReturned
```

**Obtener con condiciones flexibles:**
```python
cargos = Cargo.objects.filter(nombre='Gerente')
# Retorna QuerySet (puede tener 0, 1 o varios)
```

**Obtener el primero:**
```python
primer_cargo = Cargo.objects.first()
# Retorna el primer objeto o None
```

**Obtener por ID:**
```python
cargo = Cargo.objects.get(id=1)
# O abreviado:
cargo = Cargo.objects.get(pk=1)  # pk = primary key
```

---

### U — UPDATE (Actualizar)

**Forma 1: Modificar y guardar**
```python
cargo = Cargo.objects.get(nombre='Gerente')
cargo.descripcion = 'Nuevo jefe del departamento'
cargo.save()
```

**Forma 2: update() (más eficiente)**
```python
Cargo.objects.filter(nombre='Gerente').update(
    descripcion='Nuevo jefe del departamento'
)
# No retorna objetos, solo cantidad de filas actualizadas
```

**Diferencia:**
- Forma 1: Obtiene el objeto, lo modifica en Python, lo guarda
- Forma 2: Actualiza directamente en la BD sin traer el objeto

---

### D — DELETE (Eliminar)

**Eliminar un objeto:**
```python
cargo = Cargo.objects.get(id=1)
cargo.delete()
```

**Eliminar múltiples:**
```python
Cargo.objects.filter(nombre='Temporal').delete()
```

**Eliminar todos:**
```python
Cargo.objects.all().delete()
# ⚠️ Peligroso en producción
```

---

## Nivel 3: QuerySets

### ¿Qué es un QuerySet?

Es una **lista perezosa** de objetos de la BD. No ejecuta la query hasta que la necesites.

```python
cargos = Cargo.objects.filter(nombre__startswith='G')
# Aún no se ejecutó la query

for cargo in cargos:  # AQUÍ se ejecuta la query
    print(cargo.nombre)
```

### Encadenamiento de métodos

Puedes encadenar filtros:

```python
cargos = (Cargo.objects
    .filter(nombre__startswith='G')
    .exclude(descripcion__isnull=True)
    .order_by('nombre')
)
```

Es equivalente a:
```sql
SELECT * FROM empleados_cargo 
WHERE nombre LIKE 'G%' 
AND descripcion IS NOT NULL 
ORDER BY nombre;
```

### Operadores de búsqueda (lookups)

| Operador | Qué hace | Ejemplo |
|---|---|---|
| `=` (exact) | Exacto | `filter(nombre='Gerente')` |
| `__iexact` | Sin distinción de mayúsculas | `filter(nombre__iexact='gerente')` |
| `__contains` | Contiene | `filter(nombre__contains='rent')` |
| `__icontains` | Contiene (sin mayúsculas) | `filter(nombre__icontains='RENT')` |
| `__startswith` | Empieza con | `filter(nombre__startswith='Ger')` |
| `__istartswith` | Empieza con (sin mayúsculas) | `filter(nombre__istartswith='ger')` |
| `__endswith` | Termina con | `filter(nombre__endswith='nte')` |
| `__iendswith` | Termina con (sin mayúsculas) | `filter(nombre__iendswith='NTE')` |
| `__gt` (greater than) | Mayor que | `filter(sueldo__gt=3000)` |
| `__gte` | Mayor o igual | `filter(sueldo__gte=3000)` |
| `__lt` (less than) | Menor que | `filter(sueldo__lt=3000)` |
| `__lte` | Menor o igual | `filter(sueldo__lte=3000)` |
| `__range` | Dentro de rango | `filter(sueldo__range=[2000, 5000])` |
| `__in` | En una lista | `filter(id__in=[1, 2, 3])` |
| `__isnull` | Es NULL | `filter(descripcion__isnull=True)` |

### Ejemplos

```python
# Empleados con sueldo mayor a 3000
empleados = Empleado.objects.filter(sueldo__gt=3000)

# Empleados cuyo correo contiene 'gmail'
empleados = Empleado.objects.filter(correo__icontains='gmail')

# Cargos sin descripción
cargos = Cargo.objects.filter(descripcion__isnull=True)

# Empleados contratados en 2024
empleados = Empleado.objects.filter(
    fecha_ingreso__year=2024
)

# Empleados con sueldo entre 2000 y 5000
empleados = Empleado.objects.filter(
    sueldo__range=[2000, 5000]
)

# Empleados cuyo nombre empieza con 'Juan'
empleados = Empleado.objects.filter(
    nombres__istartswith='Juan'
)
```

### Excluir resultados

```python
# Todos los empleados EXCEPTO los que ganan más de 5000
empleados = Empleado.objects.exclude(sueldo__gt=5000)

# Equivalente a:
# SELECT * FROM empleados WHERE sueldo <= 5000
```

### Ordenar resultados

```python
# Ascendente (de menor a mayor)
empleados = Empleado.objects.order_by('sueldo')

# Descendente
empleados = Empleado.objects.order_by('-sueldo')

# Múltiples campos
empleados = Empleado.objects.order_by('cargo', '-sueldo')
# Primero por cargo, luego por sueldo descendente
```

### Limitar resultados

```python
# Los primeros 5
empleados = Empleado.objects.all()[:5]

# Del 5to al 10mo
empleados = Empleado.objects.all()[5:10]

# Con limit y offset en SQL:
# SELECT * FROM empleados LIMIT 5 OFFSET 5;
```

### Valores distintos

```python
# Todos los cargos únicos (sin duplicados)
cargos = Empleado.objects.values_list('cargo', flat=True).distinct()

# Retorna: QuerySet [1, 2, 3]  (IDs de cargos)
```

---

## Nivel 4: Relaciones

### ForeignKey (Relación 1 a N)

Recuerda nuestro modelo:

```python
class Cargo(models.Model):
    nombre = models.CharField(max_length=100)

class Empleado(models.Model):
    nombres = models.CharField(max_length=100)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)
```

**Un Cargo tiene muchos Empleados.**
**Un Empleado pertenece a un Cargo.**

### Acceder a la FK desde el empleado

```python
empleado = Empleado.objects.get(id=1)

# Obtener el cargo del empleado
cargo = empleado.cargo
print(cargo.nombre)  # "Gerente"
```

### Acceder a empleados desde el cargo (relación inversa)

```python
cargo = Cargo.objects.get(nombre='Gerente')

# Obtener todos los empleados de este cargo
empleados = cargo.empleado_set.all()
# Retorna QuerySet de Empleados

for emp in empleados:
    print(f"{emp.nombres} {emp.apellidos}")
```

**Nota:** `empleado_set` es el nombre automático (nombre_modelo_minúscula_set).

Puedes personalizarlo:
```python
class Empleado(models.Model):
    cargo = models.ForeignKey(
        Cargo, 
        on_delete=models.PROTECT,
        related_name='empleados'  # Ahora usas cargo.empleados.all()
    )
```

### Filtros a través de relaciones

**Empleados que trabajan en un cargo específico:**
```python
empleados = Empleado.objects.filter(cargo__nombre='Gerente')
# El __ (doble guión) atraviesa la relación
```

**Cargos que tienen empleados con sueldo > 5000:**
```python
cargos = Cargo.objects.filter(empleado__sueldo__gt=5000)
```

**Empleados cuyo cargo tiene descripción:**
```python
empleados = Empleado.objects.filter(
    cargo__descripcion__isnull=False
)
```

---

## Nivel 5: Agregaciones y Anotaciones

### Agregaciones (Funciones que resumen datos)

```python
from django.db.models import Count, Sum, Avg, Max, Min

# Contar empleados
total = Empleado.objects.count()
# Retorna: 25

# Suma total de sueldos
total_sueldos = Empleado.objects.aggregate(Sum('sueldo'))
# Retorna: {'sueldo__sum': 75000.00}

# Sueldo promedio
promedio = Empleado.objects.aggregate(Avg('sueldo'))
# Retorna: {'sueldo__avg': 3000.00}

# Sueldo máximo y mínimo
stats = Empleado.objects.aggregate(
    sueldo_max=Max('sueldo'),
    sueldo_min=Min('sueldo')
)
# Retorna: {'sueldo_max': 8000, 'sueldo_min': 1500}
```

### Anotaciones (Agregar información a cada objeto)

Añade un campo calculado a cada resultado:

```python
from django.db.models import Count

# Cada cargo con la cantidad de empleados
cargos = Cargo.objects.annotate(
    cantidad_empleados=Count('empleado')
)

for cargo in cargos:
    print(f"{cargo.nombre}: {cargo.cantidad_empleados} empleados")
    # Gerente: 5 empleados
    # Desarrollador: 8 empleados
```

**Diferencia:**
- `aggregate()` — retorna un diccionario con un resultado global
- `annotate()` — retorna QuerySet con un campo nuevo en cada objeto

### Ejemplos más complejos

```python
# Empleados agrupados por cargo con sueldo promedio
from django.db.models import Avg

cargos = Cargo.objects.annotate(
    sueldo_promedio=Avg('empleado__sueldo')
).order_by('-sueldo_promedio')

for cargo in cargos:
    print(f"{cargo.nombre}: ${cargo.sueldo_promedio:.2f}")
```

---

## Nivel 6: Optimización

### El problema N+1

**❌ Ineficiente (N+1 queries):**
```python
empleados = Empleado.objects.all()

for emp in empleados:  # 1 query
    print(emp.cargo.nombre)  # N queries (una por cada empleado)
# Total: 1 + N queries
```

**✅ Eficiente (select_related):**
```python
empleados = Empleado.objects.select_related('cargo')
# Trae empleados y sus cargos con 1 join

for emp in empleados:  # 0 queries adicionales
    print(emp.cargo.nombre)
# Total: 1 query
```

### select_related vs prefetch_related

**select_related** — para ForeignKey (relación 1 a 1)
```python
# 1 query con JOIN
empleados = Empleado.objects.select_related('cargo')
```

**prefetch_related** — para relaciones inversas (1 a N)
```python
# 2 queries: una para cargos, otra para empleados de cada cargo
cargos = Cargo.objects.prefetch_related('empleados')

for cargo in cargos:
    for emp in cargo.empleados.all():  # Sin query adicional
        print(emp.nombres)
```

### Obtener solo los campos necesarios

```python
# ❌ Trae todos los campos
empleados = Empleado.objects.all()

# ✅ Trae solo 2 campos
empleados = Empleado.objects.values_list('nombres', 'sueldo')
# Retorna: QuerySet [(tuple), (tuple), ...]

# ✅ Como diccionarios
empleados = Empleado.objects.values('nombres', 'sueldo')
# Retorna: QuerySet [{'nombres': 'Juan', 'sueldo': 3000}, ...]
```

---

## Ejercicios Prácticos

### Forma de practicar

Abre la consola de Django:
```powershell
.\CRUD\Scripts\python.exe manage.py shell
```

Te aparecer un intérprete Python dentro del proyecto Django.

```python
>>> from empleados.models import Cargo, Empleado
>>> from django.db.models import Count, Avg, Sum
```

---

### Ejercicio 1: CRUD Básico

**Crea un cargo llamado "Contador"**
```python
# Tu código aquí
```

**Solución:**
```python
Cargo.objects.create(nombre='Contador', descripcion='Gestiona finanzas')
```

---

### Ejercicio 2: Lectura

**Obtén todos los cargos cuya descripción no esté vacía**
```python
# Tu código aquí
```

**Solución:**
```python
Cargo.objects.filter(descripcion__isnull=False)
```

---

### Ejercicio 3: Actualizar

**Cambia la descripción del cargo "Gerente" a "Líder máximo del equipo"**
```python
# Tu código aquí
```

**Solución:**
```python
Cargo.objects.filter(nombre='Gerente').update(
    descripcion='Líder máximo del equipo'
)
# O:
cargo = Cargo.objects.get(nombre='Gerente')
cargo.descripcion = 'Líder máximo del equipo'
cargo.save()
```

---

### Ejercicio 4: Relaciones

**Obtén todos los empleados que trabajan en el cargo "Desarrollador"**
```python
# Tu código aquí
```

**Solución:**
```python
Empleado.objects.filter(cargo__nombre='Desarrollador')
```

---

### Ejercicio 5: Agregaciones

**Calcula el sueldo promedio de todos los empleados**
```python
# Tu código aquí
```

**Solución:**
```python
from django.db.models import Avg
Empleado.objects.aggregate(Avg('sueldo'))
# Retorna: {'sueldo__avg': 3000.00}
```

---

### Ejercicio 6: Anotaciones

**Obtén cada cargo con la cantidad de empleados que tiene**
```python
# Tu código aquí
```

**Solución:**
```python
from django.db.models import Count
Cargo.objects.annotate(
    cantidad=Count('empleado')
).order_by('-cantidad')
```

---

### Ejercicio 7: Complejo

**Obtén los 3 cargos con el sueldo promedio más alto**
```python
# Tu código aquí
```

**Solución:**
```python
from django.db.models import Avg
Cargo.objects.annotate(
    sueldo_promedio=Avg('empleado__sueldo')
).order_by('-sueldo_promedio')[:3]
```

---

### Ejercicio 8: N+1 Problem

**¿Cuántas queries hace este código?**
```python
cargos = Cargo.objects.all()
for cargo in cargos:
    print(f"{cargo.nombre} tiene {cargo.empleado_set.count()} empleados")
```

**Respuesta:** 1 + len(cargos) queries (problema N+1)

**Solución optimizada:**
```python
from django.db.models import Count
cargos = Cargo.objects.annotate(
    cantidad=Count('empleado')
)
for cargo in cargos:
    print(f"{cargo.nombre} tiene {cargo.cantidad} empleados")
# Solo 1 query
```

---

## Tabla de referencia rápida

| Operación | Código | Retorna |
|---|---|---|
| **Crear** | `Model.objects.create(...)` | Objeto guardado |
| **Obtener uno** | `Model.objects.get(id=1)` | Objeto o excepción |
| **Obtener todos** | `Model.objects.all()` | QuerySet |
| **Filtrar** | `Model.objects.filter(...)` | QuerySet |
| **Excluir** | `Model.objects.exclude(...)` | QuerySet |
| **Contar** | `Model.objects.count()` | Entero |
| **Primero** | `Model.objects.first()` | Objeto o None |
| **Existe** | `Model.objects.filter(...).exists()` | Boolean |
| **Actualizar** | `Model.objects.filter(...).update(...)` | Cantidad actualizada |
| **Eliminar** | `Model.objects.filter(...).delete()` | Tupla (cantidad, dict) |
| **Ordenar** | `.order_by('campo')` | QuerySet |
| **Limitar** | `[:5]` | QuerySet |
| **Agregado** | `.aggregate(Sum('campo'))` | Diccionario |
| **Anotación** | `.annotate(count=Count(...))` | QuerySet con campo nuevo |
| **Optimizar** | `.select_related('fk')` | QuerySet optimizado |

---

**¡Ahora ya conoces ORM Django! 🚀**

Practica con `manage.py shell` y experimenta con diferentes queries. La mejor forma de aprender es jugando con los datos.
