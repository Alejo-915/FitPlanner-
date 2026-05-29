from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Objetivo

router = APIRouter(prefix="/objetivos", tags=["Objetivos"])


@router.post("/")
def crear_objetivo(objetivo: Objetivo, session: Session = Depends(get_session)):
    session.add(objetivo)
    session.commit()
    session.refresh(objetivo)
    return objetivo


@router.get("/")
def listar_objetivos(session: Session = Depends(get_session)):
    return session.exec(select(Objetivo)).all()


@router.get("/{id}")
def obtener_objetivo(id: int, session: Session = Depends(get_session)):
    obj = session.get(Objetivo, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Objetivo no encontrado")
    return obj


@router.patch("/{id}")
def actualizar_objetivo(id: int, datos: Objetivo, session: Session = Depends(get_session)):
    obj = session.get(Objetivo, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Objetivo no encontrado")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(obj, key, value)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.delete("/{id}")
def eliminar_objetivo(id: int, session: Session = Depends(get_session)):
    obj = session.get(Objetivo, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Objetivo no encontrado")
    session.delete(obj)
    session.commit()
    return {"mensaje": "Objetivo eliminado correctamente"}