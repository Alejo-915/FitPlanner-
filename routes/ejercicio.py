from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Ejercicio, Usuario, Recomendacion

router = APIRouter(prefix="/ejercicios", tags=["Ejercicios"])

@router.post("/")
def crear_ejercicio(ejercicio: Ejercicio, session: Session = Depends(get_session)):
    session.add(ejercicio)
    session.commit()
    session.refresh(ejercicio)
    return ejercicio

@router.get("/")
def listar_ejercicios(session: Session = Depends(get_session)):
    return session.exec(select(Ejercicio)).all()

@router.get("/{id}")
def obtener_ejercicio(id: int, session: Session = Depends(get_session)):
    ejercicio = session.get(Ejercicio, id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return ejercicio

@router.patch("/{id}")
def actualizar_ejercicio(id: int, datos: Ejercicio, session: Session = Depends(get_session)):
    ejercicio = session.get(Ejercicio, id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(ejercicio, key, value)
    session.add(ejercicio)
    session.commit()
    session.refresh(ejercicio)
    return ejercicio

@router.delete("/{id}")
def eliminar_ejercicio(id: int, session: Session = Depends(get_session)):
    ejercicio = session.get(Ejercicio, id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    session.delete(ejercicio)
    session.commit()
    return {"mensaje": "Ejercicio eliminado correctamente"}
