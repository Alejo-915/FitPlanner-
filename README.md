# 🏋️‍♂️ FitPlanner

**FitPlanner** es una aplicación web completa para la gestión de rutinas de entrenamiento, seguimiento de progreso y recomendaciones personalizadas de fitness.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.117.1-green)
![SQLModel](https://img.shields.io/badge/SQLModel-0.0.25-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API Endpoints](#-api-endpoints)
- [Despliegue](#-despliegue)
- [Contribución](#-contribución)

---

## ✨ Características

### Para Usuarios
- 📝 **Registro e Inicio de Sesión**: Sistema de autenticación completo
- 🎯 **Objetivos Personalizados**: Define y sigue tus metas fitness
- 📊 **Seguimiento de Progreso**: Monitorea tu evolución con métricas detalladas
- 💪 **Rutinas Personalizadas**: Crea y gestiona tus planes de entrenamiento
- 📈 **Recomendaciones**: Recibe sugerencias basadas en tu IMC y objetivos

### Para Administradores
- 👥 **Gestión de Usuarios**: CRUD completo de usuarios
- 🏃 **Catálogo de Ejercicios**: Administra ejercicios con videos tutoriales
- 📋 **Gestión de Rutinas**: Crea y asigna rutinas a usuarios
- 🎯 **Objetivos del Sistema**: Define objetivos disponibles para usuarios

---

## 🛠 Tecnologías

### Backend
- **FastAPI**: Framework web moderno y rápido
- **SQLModel**: ORM para bases de datos SQL
- **Pydantic**: Validación de datos
- **Python-dotenv**: Gestión de variables de entorno
- **Uvicorn**: Servidor ASGI de alto rendimiento

### Frontend
- **Bulma CSS**: Framework CSS moderno
- **Font Awesome**: Librería de iconos
- **DataTables**: Tablas interactivas con funcionalidad avanzada
- **JavaScript Vanilla**: Sin frameworks adicionales

### Base de Datos
- **SQLite**: Desarrollo local
- **PostgreSQL**: Producción (compatible)

---

## 📦 Requisitos Previos

- Python 3.13 o superior
- pip (gestor de paquetes de Python)
- Git
- Navegador web moderno

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/fitplanner.git
cd fitplanner
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=sqlite:///fitplanner.db
```

### 6. Crear la base de datos

```bash
python -c "from db import create_db_and_tables; create_db_and_tables()"
```

---

## ⚙️ Configuración

### Base de Datos

Por defecto, FitPlanner usa SQLite para desarrollo local. Para usar PostgreSQL en producción:

1. Instala PostgreSQL
2. Crea una base de datos
3. Actualiza el archivo `.env`:

```env
DATABASE_URL=postgresql://usuario:contraseña@localhost/fitplanner
```

### Migraciones

Si necesitas agregar columnas o modificar la estructura:

```bash
# Ejemplo: Agregar columna video_url a ejercicios
python scripts/add_video_url_to_ejercicio.py

# Hacer campos nullable en usuarios
python scripts/migrate_usuario_nullable.py
```

---

## 💻 Uso

### Iniciar el servidor de desarrollo

```bash
uvicorn main:app --reload
```

La aplicación estará disponible en: `http://127.0.0.1:8000`

### Acceder a las diferentes secciones

- **Página principal**: `http://127.0.0.1:8000/`
- **Login**: `http://127.0.0.1:8000/login`
- **Registro**: `http://127.0.0.1:8000/register`
- **Panel de Usuario**: `http://127.0.0.1:8000/home/user`
- **Panel de Admin**: `http://127.0.0.1:8000/home/admin`
- **Documentación API**: `http://127.0.0.1:8000/docs`

---

## 📁 Estructura del Proyecto

```
FitPlanner/
│
├── routes/                      # Rutas de la API
│   ├── auth.py                 # Autenticación
│   ├── usuario.py              # CRUD Usuarios
│   ├── ejercicio.py            # CRUD Ejercicios
│   ├── rutina.py               # CRUD Rutinas
│   ├── rutina_ejercicio.py     # Relación Rutinas-Ejercicios
│   ├── progreso.py             # Seguimiento de progreso
│   ├── recomendacion.py        # Recomendaciones
│   └── pages.py                # Rutas de páginas HTML
│
├── templates/                   # Plantillas HTML
│   ├── auth/                   # Login y Registro
│   ├── admin/                  # Panel de administración
│   └── user/                   # Panel de usuario
│
├── static/                      # Archivos estáticos
│   ├── css/                    # Estilos
│   └── js/                     # Scripts JavaScript
│
├── scripts/                     # Scripts de migración
│
├── models.py                    # Modelos de base de datos
├── db.py                       # Configuración de base de datos
├── main.py                     # Punto de entrada de la aplicación
├── requirements.txt            # Dependencias Python
└── .env                        # Variables de entorno (no incluido)
```

---

## 🔌 API Endpoints

### Autenticación
- `POST /auth/login` - Iniciar sesión
- `POST /auth/register` - Registrar usuario

### Usuarios
- `GET /usuarios/` - Listar usuarios activos
- `GET /usuarios/{id}` - Obtener usuario por ID
- `POST /usuarios/` - Crear usuario
- `PATCH /usuarios/{id}` - Actualizar usuario
- `DELETE /usuarios/{id}` - Desactivar usuario

### Ejercicios
- `GET /ejercicios/` - Listar ejercicios
- `GET /ejercicios/{id}` - Obtener ejercicio
- `POST /ejercicios/` - Crear ejercicio
- `PATCH /ejercicios/{id}` - Actualizar ejercicio
- `DELETE /ejercicios/{id}` - Eliminar ejercicio

### Rutinas
- `GET /rutinas/` - Listar rutinas con ejercicios
- `GET /rutinas/{id}` - Obtener rutina específica
- `POST /rutinas/` - Crear rutina
- `PATCH /rutinas/{id}` - Actualizar rutina
- `DELETE /rutinas/{id}` - Eliminar rutina

### Progreso
- `GET /progresos/` - Listar registros de progreso
- `POST /progresos/` - Crear registro de progreso

### Recomendaciones
- `GET /recomendaciones/{usuario_id}` - Obtener recomendación
- `POST /recomendaciones/` - Crear recomendación

📚 **Documentación completa**: Accede a `/docs` para ver la documentación interactiva de Swagger.

---

## 🌐 Despliegue

### Desarrollo Local

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Producción con Gunicorn

```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```


## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto fue desarrollado como parte de un proyecto integrador de Desarrollo de Software.

---

## 👥 Autores

- edwin alejandro lopez monetro 

---




---

## 🙏 Agradecimientos

- FastAPI por su excelente framework
- Bulma CSS por el diseño responsive
- Font Awesome por los iconos
- DataTables por las tablas interactivas
