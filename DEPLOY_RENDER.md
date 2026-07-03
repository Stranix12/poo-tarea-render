# Desplegar en Render.com

Guía paso a paso para desplegar este proyecto Django en Render.com.

---

## Requisitos previos

1. ✅ Cuenta en [render.com](https://render.com) (gratis)
2. ✅ Repositorio en GitHub con el código
3. ✅ Archivos de configuración listos (ya incluidos)

---

## Paso 1 — Subir código a GitHub

Si aún no lo has hecho, sube tu proyecto a GitHub:

```bash
cd c:\Users\Davis\Documents\poovideo

git init
git add .
git commit -m "Proyecto Django listo para Render"
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git branch -M main
git push -u origin main
```

---

## Paso 2 — Crear nuevo Web Service en Render

1. Ve a [render.com](https://render.com) y login
2. Click en **New +** → **Web Service**
3. Selecciona **Connect a repository** → Elige tu repositorio de GitHub
4. Llena el formulario:

   | Campo | Valor |
   |---|---|
   | **Name** | `poovideo` (o lo que prefieras) |
   | **Environment** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --no-input` |
   | **Start Command** | `gunicorn djangocrud.wsgi` |

5. Click en **Create Web Service**

---

## Paso 3 — Configurar Variables de Entorno

En Render, ve a **Environment**:

### Variables requeridas:

```
SECRET_KEY = [Genera una nueva clave segura]
DEBUG = False
ALLOWED_HOSTS = localhost,127.0.0.1,tuapp.onrender.com
```

**Para generar SECRET_KEY:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

O simplemente copia una cadena aleatoria de 50 caracteres.

### Variable opcional (si quieres PostgreSQL):

Si quieres usar PostgreSQL en Render en lugar de SQLite:

```
DATABASE_URL = [Render genera esto automáticamente]
```

---

## Paso 4 — Configurar PostgreSQL (Recomendado para producción)

Para mejor rendimiento en producción, usa PostgreSQL:

1. En Render, ve a **Databases** → **New Database**
2. Llena:
   - **Name**: `poovideo_db`
   - **Database**: `poovideo`
   - **User**: `poovideo_user`
   
3. Render genera automáticamente la variable `DATABASE_URL`

Render vinculará automáticamente el Web Service con la BD.

---

## Paso 5 — Deploy automático

Una vez configurado, Render **despliega automáticamente** cada vez que hagas `git push` a `main`.

Puedes ver el progreso en **Logs**.

---

## Resultado final

Tu app estará disponible en:

```
https://poovideo.onrender.com
```

(El nombre depende de lo que hayas puesto en "Name")

---

## Solución de problemas

### Error: "DisallowedHost"
Asegúrate de que `ALLOWED_HOSTS` en Environment incluya tu dominio de Render.

### Error: "No such table"
Ejecuta la migración manualmente:
1. En Render, ve a **Shell** 
2. Ejecuta:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Error: "Static files not found"
Ya está configurado en `settings.py`. Solo asegúrate de que `STATIC_ROOT` existe.

### La BD no persiste datos
SQLite no es ideal en producción. Cambia a PostgreSQL según el **Paso 4**.

---

## Comandos útiles en Render Shell

```bash
# Ver logs
tail -f /var/log/app.log

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic --no-input
```

---

## Arquitectura final

```
GitHub (tu código)
    ↓
Render (lee cambios)
    ↓
Build: pip install + migrations
    ↓
Start: gunicorn levanta la app
    ↓
PostgreSQL (base de datos)
    ↓
URL pública: tuapp.onrender.com
```

---

**¡Tu app está en la nube! 🚀**
