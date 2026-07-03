# CRUD Django — Empleados y Cargos

Proyecto completo de Django con CRUD de Empleados y Cargos, autenticación, y dos enfoques de desarrollo: Vistas Basadas en Funciones (VBF) y Vistas Basadas en Clases (VBC).

---

## 🚀 Inicio rápido

### Prerrequisitos

- Python 3.11+
- Git
- Entorno virtual (incluido en `/CRUD`)

### Instalación y ejecución local

1. **Activar el entorno virtual:**
   ```powershell
   .\CRUD\Scripts\Activate.ps1
   ```

2. **Ejecutar el servidor:**
   ```powershell
   python manage.py runserver
   ```

3. **Abrir en el navegador:**
   ```
   http://127.0.0.1:8000
   ```

4. **Credenciales por defecto:**
   - Usuario: `admin`
   - Contraseña: `123`

---

## 📋 Estructura del proyecto

```
poovideo/
├── CRUD/                          → Entorno virtual de Python
├── djangocrud/                    → Configuración del proyecto Django
│   ├── settings.py               → Configuración global
│   ├── urls.py                   → URLs raíz del proyecto
│   ├── wsgi.py / asgi.py         → Puntos de entrada
│   └── __init__.py
├── empleados/                     → App principal
│   ├── migrations/               → Migraciones de BD
│   ├── templates/
│   │   └── empleados/
│   │       ├── base.html         → Plantilla base (navbar, Bootstrap)
│   │       ├── login.html        → Pantalla de autenticación
│   │       ├── inicio.html       → Dashboard con opciones
│   │       ├── cargos/
│   │       │   ├── listar.html
│   │       │   ├── formulario.html
│   │       │   └── confirmar_eliminar.html
│   │       └── empleados/
│   │           ├── listar.html
│   │           ├── formulario.html
│   │           └── confirmar_eliminar.html
│   ├── admin.py                  → Registro de modelos en admin
│   ├── apps.py                   → Configuración de la app
│   ├── forms.py                  → Formularios ModelForm
│   ├── models.py                 → Definición de modelos (Cargo, Empleado)
│   ├── urls.py                   → URLs de la app
│   ├── views.py                  → Vistas (VBF y VBC)
│   └── tests.py
├── static/                        → Archivos estáticos (CSS, JS, imágenes)
├── db.sqlite3                     → Base de datos SQLite (desarrollo)
├── manage.py                      → Herramienta CLI de Django
├── requirements.txt               → Dependencias Python
├── Procfile                       → Configuración para Render
├── runtime.txt                    → Versión de Python para Render
├── .env.example                   → Variables de entorno (ejemplo)
├── DEPLOY_RENDER.md              → Guía de deployment
├── LECCION_ORM_DJANGO.md         → Tutorial completo de ORM
├── cargar_datos.py               → Script para datos de prueba
└── README.md                      → Este archivo
```

---

## 🔐 Sistema de Autenticación

### ¿Cómo funciona?

1. **Login:** Accede a `/login/` con usuario y contraseña
2. **Validación:** Django compara las credenciales con la tabla `auth_user`
3. **Sesión:** Si es correcto, se crea una sesión y redirige a `/` (inicio)
4. **Protección:** Todas las vistas requieren autenticación (`@login_required`)
5. **Logout:** Botón "Salir" en el navbar para cerrar sesión

### Credenciales en la BD

Las credenciales se almacenan en la tabla `auth_user` (creada automáticamente):

```
Tabla: auth_user
┌────┬──────────┬──────────────────────────┬───────────────┐
│ id │ username │ password (HASH)          │ is_superuser  │
├────┼──────────┼──────────────────────────┼───────────────┤
│ 1  │ admin    │ pbkdf2_sha256$...       │ True          │
└────┴──────────┴──────────────────────────┴───────────────┘
```

**Puntos importantes:**
- Las contraseñas NUNCA se guardan en texto plano
- Se usan hashes con algoritmo `pbkdf2_sha256` (seguro)
- Django compara hashes al validar, no textos originales

### Gestionar usuarios

**Desde la consola:**
```powershell
python manage.py createsuperuser
```

**Desde el admin:**
```
http://127.0.0.1:8000/admin/
```

---

## 📚 Vistas disponibles

### Autenticación
| URL | Descripción |
|---|---|
| `/login/` | Pantalla de login |
| `/logout/` | Cerrar sesión |

### VBF (Vistas Basadas en Funciones)
| URL | Operación |
|---|---|
| `/` | Dashboard (inicio) |
| `/cargos/` | Listar cargos |
| `/cargos/crear/` | Crear cargo |
| `/cargos/editar/<pk>/` | Editar cargo |
| `/cargos/eliminar/<pk>/` | Eliminar cargo |
| `/empleados/` | Listar empleados |
| `/empleados/crear/` | Crear empleado |
| `/empleados/editar/<pk>/` | Editar empleado |
| `/empleados/eliminar/<pk>/` | Eliminar empleado |

### VBC (Vistas Basadas en Clases)
| URL | Operación |
|---|---|
| `/vbc/cargos/` | Listar cargos |
| `/vbc/cargos/crear/` | Crear cargo |
| `/vbc/cargos/editar/<pk>/` | Editar cargo |
| `/vbc/cargos/eliminar/<pk>/` | Eliminar cargo |
| `/vbc/empleados/` | Listar empleados |
| `/vbc/empleados/crear/` | Crear empleado |
| `/vbc/empleados/editar/<pk>/` | Editar empleado |
| `/vbc/empleados/eliminar/<pk>/` | Eliminar empleado |

### Admin
| URL | Descripción |
|---|---|
| `/admin/` | Panel de administración de Django |

---

## 📊 Modelos

### Cargo
```python
class Cargo(models.Model):
    nombre = CharField(max_length=100)
    descripcion = CharField(max_length=200, blank=True, null=True)
```

### Empleado
```python
class Empleado(models.Model):
    nombres = CharField(max_length=100)
    apellidos = CharField(max_length=100)
    correo = EmailField()
    sueldo = DecimalField(max_digits=10, decimal_places=2)
    fecha_ingreso = DateField()
    cargo = ForeignKey(Cargo, on_delete=PROTECT)
```

**Relación:** 1 Cargo → Muchos Empleados

---

## 🛠️ Comandos útiles

```bash
# Crear superusuario
python manage.py createsuperuser

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Cargar datos de prueba
python manage.py runserver  # Luego: python cargar_datos.py

# Consola interactiva de Django
python manage.py shell

# Limpiar archivos estáticos
python manage.py collectstatic --clear --noinput
```

---

## 🚀 Desplegar en Render.com

### Requisitos
- Repositorio en GitHub
- Cuenta en Render.com

### Pasos rápidos

1. **Subir a GitHub:**
   ```bash
   git add .
   git commit -m "mensaje"
   git push origin main
   ```

2. **En Render:**
   - Crear nuevo Web Service
   - Conectar repositorio GitHub
   - Configurar Build Command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --no-input`
   - Configurar Start Command: `gunicorn djangocrud.wsgi`

3. **Variables de entorno en Render:**
   ```
   SECRET_KEY = (genera una nueva)
   DEBUG = False
   ALLOWED_HOSTS = localhost,127.0.0.1,tuapp.onrender.com
   DATABASE_URL = (opcional, para PostgreSQL)
   ```

4. **Crear superusuario en Render:**
   - Ir a Shell
   - Ejecutar: `python manage.py createsuperuser`

Ver detalles completos en `DEPLOY_RENDER.md`

---

## 🎓 Aprender ORM Django

Se incluye una guía completa de ORM con:
- Conceptos básicos
- CRUD (Crear, Leer, Actualizar, Eliminar)
- QuerySets y filtros avanzados
- Relaciones entre modelos
- Agregaciones y anotaciones
- Optimización

**Archivo:** `LECCION_ORM_DJANGO.md`

**Para practicar:**
```powershell
python manage.py shell
```

---

## 📝 Tecnologías usadas

| Tecnología | Versión | Propósito |
|---|---|---|
| Python | 3.11+ | Lenguaje de programación |
| Django | 6.0.6 | Framework web |
| SQLite | - | BD local (desarrollo) |
| PostgreSQL | - | BD producción (Render) |
| Bootstrap | 5.3 | Estilos CSS |
| Bootstrap Icons | 1.11 | Iconos |
| Gunicorn | 26.0 | Servidor WSGI |

---

## ✅ Checklist de funcionalidades

- [x] Modelos Cargo y Empleado
- [x] CRUD completo con VBF
- [x] CRUD completo con VBC
- [x] Sistema de login/autenticación
- [x] Protección de vistas con @login_required
- [x] Panel admin funcional
- [x] Interfaz con Bootstrap 5
- [x] Validación de datos
- [x] Protección contra SQL injection (ORM)
- [x] Archivos estáticos configurados
- [x] Listo para desplegar en Render

---

## 🐛 Solución de problemas

### "DisallowedHost" en Render
Agrega tu dominio a `ALLOWED_HOSTS` en variables de entorno.

### "No such table" en Render
En Shell de Render:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Migraciones no se aplican
```bash
python manage.py migrate --run-syncdb
```

### Cambios no se ven en Render
Espera 2-5 minutos para que se redesplegue automáticamente.

---

## 📚 Documentación adicional

- **ORM Django:** `LECCION_ORM_DJANGO.md`
- **Deployment:** `DEPLOY_RENDER.md`
- **Datos de prueba:** `cargar_datos.py`

---

## 🎯 Resumen del desarrollo

Se desarrolló un **CRUD profesional** con:
1. **Autenticación segura** — Login con hash de contraseñas
2. **VBF y VBC** — Dos enfoques de desarrollo Django
3. **Interfaz moderna** — Bootstrap 5 + Bootstrap Icons
4. **Listo para producción** — Deployment en Render.com
5. **Educativo** — Incluye guía completa de ORM

---

**Versión:** 1.0  
**Última actualización:** 2026-07-03  
**Estado:** ✅ Listo para producción
