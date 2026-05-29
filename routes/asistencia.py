from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional
from datetime import date, timedelta
from collections import defaultdict
from db import get_session
from models import Asistencia, Usuario

router = APIRouter(prefix="/asistencias", tags=["Asistencias"])


# ── Modelo de entrada explícito (evita problemas de validación con SQLModel) ──
class AsistenciaCreate(BaseModel):
    usuario_id: int
    fecha: str          # "YYYY-MM-DD"
    duracion_minutos: Optional[int] = None
    completada: bool = True


@router.post("/")
def registrar_asistencia(
    payload: AsistenciaCreate,
    session: Session = Depends(get_session),
):
    usuario = session.get(Usuario, payload.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Convertir string a date
    try:
        fecha_obj = date.fromisoformat(payload.fecha)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")

    asistencia = Asistencia(
        usuario_id=payload.usuario_id,
        fecha=fecha_obj,
        duracion_minutos=payload.duracion_minutos,
        completada=payload.completada,
    )
    session.add(asistencia)
    session.commit()
    session.refresh(asistencia)
    return asistencia


@router.get("/usuario/{usuario_id}")
def listar_asistencias_usuario(
    usuario_id: int,
    session: Session = Depends(get_session),
):
    return session.exec(
        select(Asistencia).where(Asistencia.usuario_id == usuario_id)
    ).all()


@router.get("/estadisticas/{usuario_id}")
def estadisticas_asistencia(
    usuario_id: int,
    session: Session = Depends(get_session),
):
    asistencias = session.exec(
        select(Asistencia).where(Asistencia.usuario_id == usuario_id)
    ).all()

    if not asistencias:
        return {
            "total_sesiones": 0,
            "por_mes": {},
            "racha_actual": 0,
            "promedio_semanal": 0.0,
        }

    # Agrupar por mes
    por_mes: dict = defaultdict(int)
    for a in asistencias:
        clave = f"{a.fecha.year}-{str(a.fecha.month).zfill(2)}"
        por_mes[clave] += 1

    # Racha actual (días consecutivos hasta hoy)
    fechas = sorted({a.fecha for a in asistencias}, reverse=True)
    racha = 0
    hoy = date.today()
    esperado = hoy
    for f in fechas:
        if f == esperado or f == esperado - timedelta(days=1):
            racha += 1
            esperado = f - timedelta(days=1)
        else:
            break

    # Promedio semanal (últimas 4 semanas)
    hace_4_semanas = hoy - timedelta(weeks=4)
    recientes = [a for a in asistencias if a.fecha >= hace_4_semanas]
    promedio_semanal = round(len(recientes) / 4, 1)

    return {
        "total_sesiones": len(asistencias),
        "por_mes": dict(sorted(por_mes.items())),
        "racha_actual": racha,
        "promedio_semanal": promedio_semanal,
    }


@router.delete("/{id}")
def eliminar_asistencia(
    id: int,
    session: Session = Depends(get_session),
):
    a = session.get(Asistencia, id)
    if not a:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    session.delete(a)
    session.commit()
    return {"mensaje": "Asistencia eliminada"}