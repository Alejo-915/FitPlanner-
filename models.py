from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import date


# =========================================================
# MODELO INTERMEDIO: RutinaEjercicio (N:M + datos)
# =========================================================
class RutinaEjercicio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rutina_id: int = Field(foreign_key="rutina.id")
    ejercicio_id: int = Field(foreign_key="ejercicio.id")
    series: int
    repeticiones: int
    duracion: int          # minutos
    semana: Optional[int] = Field(default=1)   # semana del mes (1-4)
    carga_kg: Optional[float] = Field(default=0.0)  # carga progresiva


# =========================================================
# MODELO USUARIO
# =========================================================
class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str
    contraseña: str
    edad: int
    peso: Optional[float] = Field(default=None)     # kg
    altura: Optional[float] = Field(default=None)   # cm
    objetivo: str           # "bajar de peso", "ganar masa muscular", etc.
    activo: bool = True

    # ── Nuevos campos médicos / condición física ──────────
    # Limitaciones físicas (lista separada por comas): "rodilla,espalda,hombro"
    limitaciones: Optional[str] = Field(default=None)
    # Tiempo sin hacer ejercicio (meses)
    meses_sin_ejercicio: Optional[int] = Field(default=0)
    # Frecuencia semanal deseada (días/semana)
    dias_semana: Optional[int] = Field(default=3)
    # Nivel de condición física: "principiante", "intermedio", "avanzado"
    nivel_condicion: Optional[str] = Field(default="principiante")
    # Fecha de última evaluación de condición
    fecha_evaluacion: Optional[date] = Field(default=None)

    rutinas: List["Rutina"] = Relationship(back_populates="usuario")
    progresos: List["Progreso"] = Relationship(back_populates="usuario")
    recomendacion: Optional["Recomendacion"] = Relationship(back_populates="usuario")
    asistencias: List["Asistencia"] = Relationship(back_populates="usuario")


# =========================================================
# MODELO EJERCICIO
# =========================================================
class Ejercicio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    grupo_muscular: str
    equipo: str
    descripcion: str
    video_url: Optional[str] = Field(default=None)

    # ── Nuevos campos ──────────────────────────────────────
    # Dificultad: "fácil", "moderado", "difícil"
    dificultad: Optional[str] = Field(default="moderado")
    # Restricciones que impiden este ejercicio (separadas por comas): "rodilla,espalda"
    restricciones: Optional[str] = Field(default=None)

    rutinas: List["Rutina"] = Relationship(
        back_populates="ejercicios", link_model=RutinaEjercicio
    )


# =========================================================
# MODELO RUTINA
# =========================================================
class Rutina(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    nombre: str
    nivel: str
    frecuencia: int     # días por semana
    # Mes al que pertenece la rutina (para planificación mensual)
    mes: Optional[int] = Field(default=1)
    anio: Optional[int] = Field(default=2025)

    usuario: Optional[Usuario] = Relationship(back_populates="rutinas")
    ejercicios: List[Ejercicio] = Relationship(
        back_populates="rutinas", link_model=RutinaEjercicio
    )


# =========================================================
# MODELO PROGRESO
# =========================================================
class Progreso(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    fecha: date
    peso_actual: float
    repeticiones: int
    duracion: int           # minutos totales de sesión
    # Nuevos campos de seguimiento
    imc_actual: Optional[float] = Field(default=None)
    nivel_solicitado: Optional[str] = Field(default=None)  # solicitud de subir nivel

    usuario: Optional[Usuario] = Relationship(back_populates="progresos")


# =========================================================
# MODELO RECOMENDACION
# =========================================================
class Recomendacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    imc: float
    descripcion: str
    # Fase recomendada: "primero perder peso", "directo a músculo", etc.
    fase_recomendada: Optional[str] = Field(default=None)

    usuario: Optional[Usuario] = Relationship(back_populates="recomendacion")


# =========================================================
# MODELO OBJETIVO
# =========================================================
class Objetivo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    descripcion: str
    imagen_url: Optional[str] = None


# =========================================================
# MODELO ASISTENCIA (para estadísticas de frecuencia)
# =========================================================
class Asistencia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    fecha: date
    duracion_minutos: Optional[int] = Field(default=None)
    completada: bool = True

    usuario: Optional[Usuario] = Relationship(back_populates="asistencias")