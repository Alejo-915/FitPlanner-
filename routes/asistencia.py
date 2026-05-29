from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import date, timedelta
from collections import defaultdict
from db import get_session
from models import Asistencia, Usuario

router = APIRouter(prefix="/asistencias", tags=["Asistencias"])


@router.post("/")
def registrar_asistencia(asistencia: Asistencia, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, asistencia.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Convertir fecha string a objeto date si es necesario
    if isinstance(asistencia.fecha, str):
        asistencia.fecha = date.fromisoformat(asistencia.fecha)
    session.add(asistencia)
    session.commit()
    session.refresh(asistencia)
    return asistencia


@router.get("/usuario/{usuario_id}")
def listar_asistencias_usuario(usuario_id: int, session: Session = Depends(get_session)):
    return session.exec(
        select(Asistencia).where(Asistencia.usuario_id == usuario_id)
    ).all()


@router.get("/estadisticas/{usuario_id}")
def estadisticas_asistencia(usuario_id: int, session: Session = Depends(get_session)):
    asistencias = session.exec(
        select(Asistencia).where(Asistencia.usuario_id == usuario_id)
    ).all()

    if not asistencias:
        return {
            "total_sesiones": 0,
            "por_mes": {},
            "racha_actual": 0,
            "promedio_semanal": 0,
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
def eliminar_asistencia(id: int, session: Session = Depends(get_session)):
    a = session.get(Asistencia, id)
    if not a:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    session.delete(a)
    session.commit()
    return {"mensaje": "Asistencia eliminada"}
