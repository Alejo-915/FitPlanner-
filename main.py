from dotenv import load_dotenv
load_dotenv()  # Carga variables de entorno del archivo .env

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from db import create_db_and_tables

from routes.usuario import router as usuario_router
from routes.ejercicio import router as ejercicio_router
from routes.rutina import router as rutina_router
from routes.rutina_ejercicio import router as rutina_ejercicio_router
from routes.progreso import router as progreso_router
from routes.recomendacion import router as recomendacion_router
from routes.auth import router as auth
from routes.pages import router as pages_router
from routes.sesion import router as sesion_router  # NUEVO

app = FastAPI(title="FitPlanner API")

# CORS middleware para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(usuario_router)
app.include_router(ejercicio_router)
app.include_router(rutina_router)
app.include_router(rutina_ejercicio_router)
app.include_router(progreso_router)
app.include_router(recomendacion_router)
app.include_router(auth)
app.include_router(pages_router)
app.include_router(sesion_router)  # NUEVO

@app.get("/")
def root():
    return {
        "mensaje": "Bienvenido a FitPlanner API 🏋️‍♂️",
        "endpoints": [
            "/usuarios",
            "/ejercicios",
            "/rutinas",
            "/rutinas_ejercicios",
            "/progresos",
            "/recomendaciones",
            "/sesiones"  # NUEVO
        ]
    }
