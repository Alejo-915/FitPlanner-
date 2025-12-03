from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import date

# =========================================================
# MODELO INTERMEDIO: RutinaEjercicio (N:M + datos)
# =========================================================
class RutinaEjercicio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rutina_id: int = Field(default=None, foreign_key="rutina.id")
    ejercicio_id: int = Field(default=None, foreign_key="ejercicio.id")
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


# =========================================================
# MODELO EJERCICIO
# =========================================================
class Ejercicio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    grupo_muscular: str
    equipo: str
    descripcion: str

    rutinas: List["Rutina"] = Relationship(
        back_populates="ejercicios", link_model=RutinaEjercicio
    )


# =========================================================
# MODELO RUTINA
# =========================================================
class Rutina(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(default=None, foreign_key="usuario.id")
    nombre: str
    nivel: str
    frecuencia: int

    usuario: Optional[Usuario] = Relationship(back_populates="rutinas")
    ejercicios: List[Ejercicio] = Relationship(
        back_populates="rutinas", link_model=RutinaEjercicio
    )


class Progreso(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(default=None, foreign_key="usuario.id")
    fecha: date
    peso_actual: float
    repeticiones: int
    duracion: int

    usuario: Optional[Usuario] = Relationship(back_populates="progresos")

class Recomendacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(default=None, foreign_key="usuario.id")
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
