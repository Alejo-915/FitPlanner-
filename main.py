from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db import create_db_and_tables

from routes.usuario import router as usuario_router
from routes.ejercicio import router as ejercicio_router
from routes.rutina import router as rutina_router
from routes.rutina_ejercicio import router as rutina_ejercicio_router
from routes.progreso import router as progreso_router
from routes.recomendacion import router as recomendacion_router
from routes.auth import router as auth_router
from routes.pages import router as pages_router
from routes.asistencia import router as asistencia_router
from routes.rutina_mensual import router as rutina_mensual_router

app = FastAPI(
    title="FitPlanner API",
    description="API para gestión de rutinas de entrenamiento con recomendaciones personalizadas.",
    version="2.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Routers
app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(ejercicio_router)
app.include_router(rutina_router)
app.include_router(rutina_ejercicio_router)
app.include_router(progreso_router)
app.include_router(recomendacion_router)
app.include_router(asistencia_router)
app.include_router(rutina_mensual_router)
app.include_router(pages_router)


@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0.0"}