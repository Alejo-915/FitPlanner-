from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Progreso

router = APIRouter(prefix="/progresos", tags=["Progresos"])

@router.post("/")
def crear_progreso(progreso: Progreso, session: Session = Depends(get_session)):
    session.add(progreso)
    session.commit()
    session.refresh(progreso)
    return progreso

@router.get("/")
def listar_progresos(session: Session = Depends(get_session)):
    return session.exec(select(Progreso)).all()

@router.get("/{id}")
def obtener_progreso(id: int, session: Session = Depends(get_session)):
    progreso = session.get(Progreso, id)
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    return progreso

@router.patch("/{id}")
def actualizar_progreso(id: int, datos: Progreso, session: Session = Depends(get_session)):
    progreso = session.get(Progreso, id)
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    for key, value in datos.dict(exclude_unset=True).items():
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
