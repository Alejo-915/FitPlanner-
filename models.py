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
    duracion: int
    semana: Optional[int] = Field(default=1)
    carga_kg: Optional[float] = Field(default=0.0)


# =========================================================
# MODELO USUARIO
# =========================================================
class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str
    contraseña: str
    edad: int
    peso: Optional[float] = Field(default=None)
    altura: Optional[float] = Field(default=None)
    objetivo: str
    activo: bool = True
    limitaciones: Optional[str] = Field(default=None)
    meses_sin_ejercicio: Optional[int] = Field(default=0)
    dias_semana: Optional[int] = Field(default=3)
    nivel_condicion: Optional[str] = Field(default="principiante")
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
    dificultad: Optional[str] = Field(default="moderado")
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
    frecuencia: int
    mes: Optional[int] = Field(default=1)
    anio: Optional[int] = Field(default=2025)

    usuario: Optional[Usuario] = Relationship(back_populates="rutinas")
    ejercicios: List[Ejercicio] = Relationship(
        back_populates="rutinas", link_model=RutinaEjercicio
    )


# =========================================================
# MODELO PROGRESO — AMPLIADO
# =========================================================
class Progreso(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    fecha: date

    # Métricas corporales
    peso_actual: float                                          # kg (obligatorio)
    cintura_cm: Optional[float] = Field(default=None)          # cm (opcional)
    porcentaje_grasa: Optional[float] = Field(default=None)    # % (opcional)

    # Métricas de sesión
    duracion: int                                               # minutos totales
    energia: Optional[int] = Field(default=3)                  # 1-5 (cómo se sintió)
    notas: Optional[str] = Field(default=None)                 # texto libre

    # Campos legacy / calculados
    repeticiones: Optional[int] = Field(default=None)          # ahora opcional
    imc_actual: Optional[float] = Field(default=None)
    nivel_solicitado: Optional[str] = Field(default=None)

    usuario: Optional[Usuario] = Relationship(back_populates="progresos")


# =========================================================
# MODELO RECOMENDACION
# =========================================================
class Recomendacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    imc: float
    descripcion: str
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
# MODELO ASISTENCIA
# =========================================================
class Asistencia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    fecha: date
    duracion_minutos: Optional[int] = Field(default=None)
    completada: bool = True

    usuario: Optional[Usuario] = Relationship(back_populates="asistencias")