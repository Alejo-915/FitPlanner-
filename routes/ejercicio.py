from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import Optional
from db import get_session
from models import Ejercicio, Usuario

router = APIRouter(prefix="/ejercicios", tags=["Ejercicios"])


@router.post("/")
def crear_ejercicio(ejercicio: Ejercicio, session: Session = Depends(get_session)):
    session.add(ejercicio)
    session.commit()
    session.refresh(ejercicio)
    return ejercicio


@router.get("/")
def listar_ejercicios(
    grupo_muscular: Optional[str] = None,
    dificultad: Optional[str] = None,
    session: Session = Depends(get_session),
):
    query = select(Ejercicio)
    if grupo_muscular:
        query = query.where(Ejercicio.grupo_muscular == grupo_muscular)
    if dificultad:
        query = query.where(Ejercicio.dificultad == dificultad)
    return session.exec(query).all()


@router.get("/compatibles/{usuario_id}")
def ejercicios_compatibles_usuario(
    usuario_id: int,
    session: Session = Depends(get_session),
):
    """
    Devuelve solo los ejercicios que NO están restringidos
    por las limitaciones físicas del usuario.
    """
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    limitaciones = (
        [l.strip().lower() for l in usuario.limitaciones.split(",")]
        if usuario.limitaciones
        else []
    )

    todos = session.exec(select(Ejercicio)).all()

    if not limitaciones:
        return todos

    compatibles = []
    for ej in todos:
        restricciones_ej = (
            [r.strip().lower() for r in ej.restricciones.split(",")]
            if ej.restricciones
            else []
        )
        if not any(lim in restricciones_ej for lim in limitaciones):
            compatibles.append(ej)

    return compatibles


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