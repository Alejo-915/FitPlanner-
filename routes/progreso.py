from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional
from datetime import date
from db import get_session
from models import Progreso

router = APIRouter(prefix="/progresos", tags=["Progresos"])


# ── Modelo de entrada explícito ──────────────────────────
class ProgresoCreate(BaseModel):
    usuario_id: int
    fecha: str                                # "YYYY-MM-DD"
    peso_actual: float                        # kg — obligatorio
    duracion: int                             # minutos — obligatorio
    cintura_cm: Optional[float] = None        # cm — opcional
    porcentaje_grasa: Optional[float] = None  # % — opcional
    energia: Optional[int] = 3               # 1-5 — opcional
    notas: Optional[str] = None              # texto — opcional


@router.post("/")
def crear_progreso(payload: ProgresoCreate, session: Session = Depends(get_session)):
    try:
        fecha_obj = date.fromisoformat(payload.fecha)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")

    progreso = Progreso(
        usuario_id=payload.usuario_id,
        fecha=fecha_obj,
        peso_actual=payload.peso_actual,
        duracion=payload.duracion,
        cintura_cm=payload.cintura_cm,
        porcentaje_grasa=payload.porcentaje_grasa,
        energia=payload.energia,
        notas=payload.notas,
        repeticiones=0,   # ← columna legacy NOT NULL, se mantiene en 0
    )
    session.add(progreso)
    session.commit()
    session.refresh(progreso)
    return progreso


@router.get("/")
def listar_progresos(session: Session = Depends(get_session)):
    return session.exec(select(Progreso)).all()


@router.get("/usuario/{usuario_id}")
def obtener_progresos_usuario(usuario_id: int, session: Session = Depends(get_session)):
    return session.exec(
        select(Progreso)
        .where(Progreso.usuario_id == usuario_id)
        .order_by(Progreso.fecha)
    ).all()


@router.get("/{id}")
def obtener_progreso(id: int, session: Session = Depends(get_session)):
    progreso = session.get(Progreso, id)
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    return progreso


@router.patch("/{id}")
def actualizar_progreso(id: int, datos: ProgresoCreate, session: Session = Depends(get_session)):
    progreso = session.get(Progreso, id)
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    for key, value in datos.dict(exclude_unset=True).items():
        if key == "fecha":
            setattr(progreso, key, date.fromisoformat(value))
        else:
            setattr(progreso, key, value)
    session.add(progreso)
    session.commit()
    session.refresh(progreso)
    return progreso


@router.delete("/{id}")
def eliminar_progreso(id: int, session: Session = Depends(get_session)):
    progreso = session.get(Progreso, id)
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    session.delete(progreso)
    session.commit()
    return {"mensaje": "Progreso eliminado correctamente"}