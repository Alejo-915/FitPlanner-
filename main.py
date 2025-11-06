from fastapi import FastAPI
from db import create_db_and_tables
from usuario import router as usuario_router
from ejercicio import router as ejercicio_router
from rutina import router as rutina_router
from rutina_ejercicio import router as rutina_ejercicio_router
from progreso import router as progreso_router
from recomendacion import router as recomendacion_router

app = FastAPI(title="FitPlanner API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(usuario_router)
app.include_router(ejercicio_router)
app.include_router(rutina_router)
app.include_router(rutina_ejercicio_router)
app.include_router(progreso_router)
app.include_router(recomendacion_router)


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
            "/recomendaciones"
        ]
    }
