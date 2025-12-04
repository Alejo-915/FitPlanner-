# =========================================================
# IMPORTS
# =========================================================
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import date, datetime


# =========================================================
# MODELO INTERMEDIO: RutinaEjercicio (N:M + datos)
# =========================================================
class RutinaEjercicio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rutina_id: int = Field(foreign_key="rutina.id")
    ejercicio_id: int = Field(foreign_key="ejercicio.id")
    series: int
    repeticiones: int
    duracion: int  # minutos o segundos, según definas


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

    rutinas: List["Rutina"] = Relationship(back_populates="usuario")
    progresos: List["Progreso"] = Relationship(back_populates="usuario")
    recomendacion: Optional["Recomendacion"] = Relationship(back_populates="usuario")
    sesiones: List["SesionEntrenamiento"] = Relationship(back_populates="usuario")


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

    usuario: Optional[Usuario] = Relationship(back_populates="rutinas")
    ejercicios: List[Ejercicio] = Relationship(
        back_populates="rutinas", link_model=RutinaEjercicio
    )
    sesiones: List["SesionEntrenamiento"] = Relationship(back_populates="rutina")


# =========================================================
# MODELO PROGRESO (Mantenido para historial)
# =========================================================
class Progreso(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    fecha: date
    peso_actual: float
    repeticiones: int
    duracion: int

    usuario: Optional[Usuario] = Relationship(back_populates="progresos")


# =========================================================
# MODELO RECOMENDACION
# =========================================================
class Recomendacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    imc: float
    descripcion: str

    usuario: Optional[Usuario] = Relationship(back_populates="recomendacion")


# =========================================================
# MODELO OBJETIVO (Nuevo)
# =========================================================
class Objetivo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    descripcion: str
    imagen_url: Optional[str] = None


# =========================================================
# NUEVO: MODELO SESION DE ENTRENAMIENTO
# =========================================================
class SesionEntrenamiento(SQLModel, table=True):
    """Representa una sesión de entrenamiento completada o en progreso"""
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    rutina_id: int = Field(foreign_key="rutina.id")
    fecha_inicio: datetime = Field(default_factory=datetime.now)
    fecha_fin: Optional[datetime] = None
    completada: bool = False

    usuario: Optional[Usuario] = Relationship(back_populates="sesiones")
    rutina: Optional[Rutina] = Relationship(back_populates="sesiones")
    ejercicios_completados: List["EjercicioCompletado"] = Relationship(back_populates="sesion")


# =========================================================
# NUEVO: EJERCICIO COMPLETADO EN UNA SESIÓN
# =========================================================
class EjercicioCompletado(SQLModel, table=True):
    """Trackea qué ejercicios se completaron en una sesión"""
    id: Optional[int] = Field(default=None, primary_key=True)
    sesion_id: int = Field(foreign_key="sesionentrenamiento.id")
    ejercicio_id: int = Field(foreign_key="ejercicio.id")
    completado: bool = False
    notas: Optional[str] = None

    sesion: Optional[SesionEntrenamiento] = Relationship(back_populates="ejercicios_completados")
