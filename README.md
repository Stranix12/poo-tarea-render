# CRUD Django — Empleados y Cargos

Proyecto Django que implementa un CRUD completo de **Empleados** y **Cargos** usando dos enfoques:
- **VBF** — Vistas Basadas en Funciones
- **VBC** — Vistas Basadas en Clases

---

## Estructura del proyecto

```
poovideo/
├── CRUD/                  → Entorno virtual de Python
├── djangocrud/            → Configuración del proyecto Django
│   ├── settings.py        → Configuración general
│   ├── urls.py            → URLs raíz del proyecto
│   ├── wsgi.py            → Punto de entrada WSGI
│   └── asgi.py            → Punto de entrada ASGI
├── empleados/             → App principal
│   ├── migrations/        → Migraciones de base de datos
│   ├── templates/
│   │   └── empleados/
│   │       ├── base.html
│   │       ├── cargos/
│   │       │   ├── listar.html
│   │       │   ├── formulario.html
│   │       │   └── confirmar_eliminar.html
│   │       └── empleados/
│   │           ├── listar.html
│   │           ├── formulario.html
│   │           └── confirmar_eliminar.html
│   ├── admin.py           → Registro en el panel admin
│   ├── apps.py            → Configuración de la app
│   ├── forms.py           → Formularios
│   ├── models.py          → Modelos (tablas de la BD)
│   ├── urls.py            → URLs de la app
│   └── views.py           → Vistas (lógica)
├── db.sqlite3             → Base de datos SQLite
└── manage.py              → Herramienta de comandos Django
```

---

## Comandos utilizados

| Comando | Para qué sirve |
|---|---|
| `django-admin startproject djangocrud` | Crea la estructura base del proyecto Django |
| `manage.py startapp empleados` | Crea una nueva app dentro del proyecto |
| `manage.py makemigrations` | Lee los modelos y genera archivos de migración |
| `manage.py migrate` | Ejecuta las migraciones y crea las tablas en la BD |
| `manage.py createsuperuser` | Crea un usuario administrador para el panel admin |
| `manage.py runserver` | Levanta el servidor de desarrollo en `http://127.0.0.1:8000` |
| `manage.py check` | Verifica que el proyecto no tenga errores de configuración |

**Cómo ejecutarlos** (sin activar el entorno virtual):
```powershell
.\CRUD\Scripts\python.exe manage.py <comando>
```

---

## URLs disponibles

| URL | Tipo | Operación |
|---|---|---|
| `/admin/` | — | Panel de administración Django |
| `/cargos/` | VBF | Listar cargos |
| `/cargos/crear/` | VBF | Crear cargo |
| `/cargos/editar/<pk>/` | VBF | Editar cargo |
| `/cargos/eliminar/<pk>/` | VBF | Eliminar cargo |
| `/empleados/` | VBF | Listar empleados |
| `/empleados/crear/` | VBF | Crear empleado |
| `/empleados/editar/<pk>/` | VBF | Editar empleado |
| `/empleados/eliminar/<pk>/` | VBF | Eliminar empleado |
| `/vbc/cargos/` | VBC | Listar cargos |
| `/vbc/cargos/crear/` | VBC | Crear cargo |
| `/vbc/cargos/editar/<pk>/` | VBC | Editar cargo |
| `/vbc/cargos/eliminar/<pk>/` | VBC | Eliminar cargo |
| `/vbc/empleados/` | VBC | Listar empleados |
| `/vbc/empleados/crear/` | VBC | Crear empleado |
| `/vbc/empleados/editar/<pk>/` | VBC | Editar empleado |
| `/vbc/empleados/eliminar/<pk>/` | VBC | Eliminar empleado |

---

## Paso a paso — De inicio a fin

### Paso 1 — Limpieza del proyecto

Se eliminó la app `task/` (vacía, nombre incorrecto) y `db.sqlite3`.
Se quitó `'task'` de `INSTALLED_APPS` en `settings.py`.

### Paso 2 — Crear la app `empleados`

```powershell
.\CRUD\Scripts\python.exe manage.py startapp empleados
```

Se registró en `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'empleados',
]
```

### Paso 3 — Definir los modelos (`models.py`)

Se crearon los modelos `Cargo` y `Empleado` con su relación `ForeignKey`.

### Paso 4 — Crear y aplicar migraciones

```powershell
.\CRUD\Scripts\python.exe manage.py makemigrations
.\CRUD\Scripts\python.exe manage.py migrate
```

### Paso 5 — Registrar modelos en el Admin

Se editó `admin.py` y se creó el superusuario:
```powershell
.\CRUD\Scripts\python.exe manage.py createsuperuser
```

### Paso 6 — Crear formularios (`forms.py`)

Se crearon `CargoForm` y `EmpleadoForm` con `ModelForm` y widgets personalizados.

### Paso 7 — Configurar URLs

Se creó `empleados/urls.py` y se incluyó en `djangocrud/urls.py`.

### Paso 8 — Crear vistas VBF (`views.py`)

Se implementaron 4 funciones por modelo: listar, crear, editar, eliminar.
Se agregó manejo de `ProtectedError` al intentar eliminar un cargo con empleados.

### Paso 9 — Crear plantillas HTML

Se creó `base.html` con navbar y Bootstrap 5.
Se crearon 3 plantillas por modelo: listar, formulario, confirmar_eliminar.

### Paso 10 — Implementar VBC (`views.py`)

Se agregaron clases que heredan de `ListView`, `CreateView`, `UpdateView`, `DeleteView`.
Se registraron con prefijo `/vbc/` en `urls.py`.

### Paso 11 — Mejorar la interfaz

Se rediseñaron todas las plantillas con Bootstrap Icons, colores, gradientes y estilos modernos.
Se agregaron clases CSS a los widgets en `forms.py`.

---

## Documentación de archivos

---

### `djangocrud/settings.py` — Configuración del proyecto

| Variable | Qué hace |
|---|---|
| `BASE_DIR` | Ruta raíz del proyecto, usada para construir otras rutas |
| `SECRET_KEY` | Clave secreta para firmar cookies y tokens (nunca publicar en producción) |
| `DEBUG` | Si es `True`, muestra errores detallados. Debe ser `False` en producción |
| `ALLOWED_HOSTS` | Lista de dominios permitidos para servir la app |
| `INSTALLED_APPS` | Lista de todas las apps activas en el proyecto |
| `MIDDLEWARE` | Capas de procesamiento que actúan sobre cada request/response |
| `ROOT_URLCONF` | Módulo Python que contiene las URLs raíz (`djangocrud.urls`) |
| `TEMPLATES` | Configuración del motor de plantillas HTML |
| `APP_DIRS: True` | Django busca plantillas dentro de la carpeta `templates/` de cada app |
| `DATABASES` | Configuración de la base de datos (SQLite por defecto) |
| `LANGUAGE_CODE` | Idioma del sistema (afecta fechas, mensajes de error, etc.) |
| `TIME_ZONE` | Zona horaria del servidor |
| `USE_TZ` | Si es `True`, Django usa fechas con zona horaria |
| `STATIC_URL` | URL base para archivos estáticos (CSS, JS, imágenes) |

---

### `djangocrud/urls.py` — URLs raíz del proyecto

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('empleados.urls')),
]
```

| Elemento | Qué hace |
|---|---|
| `path('admin/', ...)` | Monta el panel de administración en `/admin/` |
| `include('empleados.urls')` | Delega todas las demás URLs al archivo `urls.py` de la app `empleados` |
| `path('', ...)` | La raíz vacía `''` significa que las URLs de empleados se montan desde la raíz |

---

### `empleados/apps.py` — Configuración de la app

```python
from django.apps import AppConfig

class EmpleadosConfig(AppConfig):
    name = 'empleados'
```

| Elemento | Qué hace |
|---|---|
| `AppConfig` | Clase base de Django para configurar una app |
| `name = 'empleados'` | Nombre interno de la app, debe coincidir con el nombre de la carpeta |

---

### `empleados/models.py` — Modelos (tablas de la BD)

```python
from django.db import models

class Cargo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField()
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ingreso = models.DateField()
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'
```

| Elemento | Qué hace |
|---|---|
| `models.Model` | Clase base de Django; toda clase que herede de ella se convierte en una tabla |
| `CharField` | Campo de texto corto con límite de caracteres |
| `max_length=100` | Máximo de caracteres permitidos en el campo |
| `blank=True` | El campo puede estar vacío en formularios |
| `null=True` | La base de datos permite guardar NULL en esa columna |
| `EmailField` | Campo de texto que valida formato de correo electrónico |
| `DecimalField` | Campo numérico con decimales de precisión fija |
| `max_digits=10` | Total de dígitos permitidos (ej: 99999999.99) |
| `decimal_places=2` | Cantidad de decimales (ej: 1500.50) |
| `DateField` | Campo de fecha (sin hora) |
| `ForeignKey` | Crea una relación muchos-a-uno entre dos modelos |
| `on_delete=models.PROTECT` | Impide eliminar un Cargo si tiene Empleados asociados |
| `__str__()` | Define cómo se muestra el objeto en texto (admin, dropdowns, etc.) |
| `f'{self.nombres} {self.apellidos}'` | F-string que combina campos para mostrar nombre completo |

---

### `empleados/admin.py` — Panel de administración

```python
from django.contrib import admin
from .models import Cargo, Empleado

admin.site.register(Cargo)
admin.site.register(Empleado)
```

| Elemento | Qué hace |
|---|---|
| `from .models import ...` | El `.` indica importar desde el mismo paquete (la misma app) |
| `admin.site.register(Cargo)` | Hace visible el modelo `Cargo` en el panel `/admin/` |
| `admin.site.register(Empleado)` | Hace visible el modelo `Empleado` en el panel `/admin/` |

---

### `empleados/forms.py` — Formularios

```python
from django import forms
from .models import Cargo, Empleado

FIELD_CLASS = {'class': 'form-control'}
SELECT_CLASS = {'class': 'form-select'}

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={**FIELD_CLASS, 'placeholder': 'Ej: Gerente General'}),
            'descripcion': forms.TextInput(attrs={**FIELD_CLASS, 'placeholder': 'Descripción breve'}),
        }

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'nombres':       forms.TextInput(attrs={**FIELD_CLASS}),
            'apellidos':     forms.TextInput(attrs={**FIELD_CLASS}),
            'correo':        forms.EmailInput(attrs={**FIELD_CLASS}),
            'sueldo':        forms.NumberInput(attrs={**FIELD_CLASS}),
            'fecha_ingreso': forms.DateInput(attrs={**FIELD_CLASS, 'type': 'date'}),
            'cargo':         forms.Select(attrs=SELECT_CLASS),
        }
```

| Elemento | Qué hace |
|---|---|
| `forms.ModelForm` | Genera automáticamente un formulario basado en un modelo |
| `class Meta` | Clase interna que configura el formulario |
| `model = Cargo` | Modelo en el que se basa el formulario |
| `fields = '__all__'` | Incluye todos los campos del modelo en el formulario |
| `widgets` | Diccionario que personaliza el HTML de cada campo |
| `forms.TextInput` | Renderiza un `<input type="text">` |
| `forms.EmailInput` | Renderiza un `<input type="email">` |
| `forms.NumberInput` | Renderiza un `<input type="number">` |
| `forms.DateInput` | Renderiza un `<input type="date">` (selector de fecha) |
| `forms.Select` | Renderiza un `<select>` (dropdown) |
| `attrs` | Diccionario de atributos HTML que se agregan al campo |
| `'class': 'form-control'` | Aplica estilos de Bootstrap al campo |
| `'placeholder'` | Texto de ayuda visible dentro del campo vacío |
| `**FIELD_CLASS` | Desempaqueta el diccionario (equivale a escribir `'class': 'form-control'`) |

---

### `empleados/urls.py` — URLs de la app

```python
from django.urls import path
from . import views

urlpatterns = [
    path('cargos/', views.cargo_listar, name='cargo_listar'),
    path('cargos/crear/', views.cargo_crear, name='cargo_crear'),
    path('cargos/editar/<int:pk>/', views.cargo_editar, name='cargo_editar'),
    path('cargos/eliminar/<int:pk>/', views.cargo_eliminar, name='cargo_eliminar'),
    ...
]
```

| Elemento | Qué hace |
|---|---|
| `path()` | Define una URL y la conecta con una vista |
| `'cargos/'` | La ruta que aparece en el navegador |
| `views.cargo_listar` | La función o clase que responde a esa URL |
| `name='cargo_listar'` | Nombre único para referenciar la URL desde templates con `{% url %}` |
| `<int:pk>` | Captura un número entero de la URL y lo pasa a la vista como parámetro `pk` |
| `views.CargoListView.as_view()` | Convierte una clase VBC en una vista que Django puede usar |
| `urlpatterns` | Lista obligatoria donde Django busca todas las rutas |

---

### `empleados/views.py` — Vistas (VBF y VBC)

#### Vistas Basadas en Funciones (VBF)

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cargo, Empleado
from .forms import CargoForm, EmpleadoForm
from django.db.models.deletion import ProtectedError
```

| Elemento | Qué hace |
|---|---|
| `render(request, template, context)` | Combina una plantilla HTML con datos y devuelve la respuesta al navegador |
| `get_object_or_404(Model, pk=pk)` | Busca un objeto por su ID; si no existe devuelve error 404 automáticamente |
| `redirect('nombre_url')` | Redirige al navegador a otra URL por su nombre |
| `request.method` | Indica si la solicitud es `GET` (ver formulario) o `POST` (enviar formulario) |
| `form.is_valid()` | Valida los datos del formulario; retorna `True` si todo está correcto |
| `form.save()` | Guarda el formulario en la base de datos |
| `CargoForm(request.POST)` | Crea el formulario con los datos enviados por el usuario |
| `CargoForm(instance=cargo)` | Crea el formulario pre-cargado con los datos de un objeto existente |
| `ProtectedError` | Excepción que lanza Django al intentar eliminar un objeto protegido por `ForeignKey` |
| `cargo.empleado_set.all()` | Obtiene todos los empleados relacionados a un cargo (relación inversa) |
| `Cargo.objects.all()` | Trae todos los registros de la tabla Cargo |
| `context` | Diccionario con datos que se envían a la plantilla HTML |

#### Vistas Basadas en Clases (VBC)

```python
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
```

| Elemento | Qué hace |
|---|---|
| `ListView` | Vista genérica para listar objetos de un modelo |
| `CreateView` | Vista genérica para crear un nuevo objeto |
| `UpdateView` | Vista genérica para editar un objeto existente |
| `DeleteView` | Vista genérica para eliminar un objeto |
| `model` | Atributo que indica qué modelo usa la vista |
| `template_name` | Ruta de la plantilla HTML que usa la vista |
| `context_object_name` | Nombre con el que los objetos están disponibles en la plantilla |
| `form_class` | Formulario que usa la vista para crear/editar |
| `success_url` | URL a la que redirige después de completar la operación |
| `reverse_lazy('nombre')` | Igual que `redirect` pero para clases; se evalúa tarde (cuando las URLs ya están cargadas) |
| `.as_view()` | Convierte la clase en una función que Django puede usar como vista |

#### Comparación VBF vs VBC

| Aspecto | VBF | VBC |
|---|---|---|
| Estilo | Funciones Python | Clases Python |
| Código | Más líneas, más explícito | Menos líneas, más automático |
| Control | Total sobre la lógica | Django maneja la lógica |
| Dificultad | Más fácil de entender | Requiere conocer las clases genéricas |
| Ruta | `/cargos/`, `/empleados/` | `/vbc/cargos/`, `/vbc/empleados/` |

---

### Plantillas HTML

| Archivo | Qué hace |
|---|---|
| `base.html` | Plantilla base con navbar y Bootstrap. Todas las demás la heredan |
| `cargos/listar.html` | Tabla con todos los cargos y botones de editar/eliminar |
| `cargos/formulario.html` | Formulario para crear o editar un cargo |
| `cargos/confirmar_eliminar.html` | Confirmación antes de eliminar; muestra advertencia si tiene empleados |
| `empleados/listar.html` | Tabla con todos los empleados y sus datos |
| `empleados/formulario.html` | Formulario para crear o editar un empleado |
| `empleados/confirmar_eliminar.html` | Confirmación antes de eliminar un empleado |

#### Etiquetas de plantilla Django usadas

| Etiqueta | Qué hace |
|---|---|
| `{% extends 'base.html' %}` | Indica que esta plantilla hereda de `base.html` |
| `{% block contenido %}` | Define una sección reemplazable en la plantilla base |
| `{% endblock %}` | Cierra el bloque |
| `{% for item in lista %}` | Itera sobre una lista de objetos |
| `{% empty %}` | Se ejecuta si la lista está vacía |
| `{% endfor %}` | Cierra el bucle |
| `{% if condicion %}` | Condicional |
| `{% elif %}` / `{% else %}` | Ramas del condicional |
| `{% endif %}` | Cierra el condicional |
| `{% url 'nombre' %}` | Genera la URL por su nombre definido en `urls.py` |
| `{% url 'nombre' pk %}` | Genera la URL pasando un parámetro (el ID del objeto) |
| `{% csrf_token %}` | Token de seguridad obligatorio en formularios POST |
| `{{ variable }}` | Imprime el valor de una variable del contexto |
| `{{ variable\|default:"—" }}` | Imprime un valor por defecto si la variable está vacía |
| `{{ forloop.counter }}` | Número de iteración actual del bucle (1, 2, 3...) |

---

## Relación entre los modelos

```
Cargo (1) ────────── (N) Empleado
  │                        │
  nombre                   nombres
  descripcion              apellidos
                           correo
                           sueldo
                           fecha_ingreso
                           cargo ──→ FK a Cargo
```

- Un **Cargo** puede tener **muchos Empleados**
- Un **Empleado** pertenece a **un solo Cargo**
- Si intentas eliminar un **Cargo con empleados**, Django lanza `ProtectedError` y se muestra un mensaje de advertencia

---

## Tecnologías usadas

| Tecnología | Versión | Para qué |
|---|---|---|
| Python | 3.14 | Lenguaje de programación |
| Django | 6.0.6 | Framework web |
| SQLite | — | Base de datos (archivo local) |
| Bootstrap | 5.3 | Estilos CSS y componentes UI |
| Bootstrap Icons | 1.11 | Iconos SVG |
