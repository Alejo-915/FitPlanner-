from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Rutina, Ejercicio, RutinaEjercicio

router = APIRouter(prefix="/rutinas_ejercicios", tags=["Relación Rutina-Ejercicio"])

# ✅ Crear una relación entre rutina y ejercicio con datos
@router.post("/")
def asignar_ejercicio_a_rutina(relacion: RutinaEjercicio, session: Session = Depends(get_session)):
    rutina = session.get(Rutina, relacion.rutina_id)
    ejercicio = session.get(Ejercicio, relacion.ejercicio_id)

    if not rutina or not ejercicio:
        raise HTTPException(status_code=404, detail="Rutina o ejercicio no encontrado")

    existente = session.exec(
        select(RutinaEjercicio).where(
            (RutinaEjercicio.rutina_id == relacion.rutina_id) &
            (RutinaEjercicio.ejercicio_id == relacion.ejercicio_id)
        )
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="El ejercicio ya está asignado a esta rutina")

    session.add(relacion)
    session.commit()
    session.refresh(relacion)
    return {"mensaje": "Ejercicio asignado correctamente a la rutina", "relacion": relacion}

# 📋 Listar relaciones
@router.get("/")
def listar_relaciones(session: Session = Depends(get_session)):
    return session.exec(select(RutinaEjercicio)).all()

# 🔁 Actualizar series, repeticiones o duración
@router.patch("/{id}")
def actualizar_relacion(id: int, datos: RutinaEjercicio, session: Session = Depends(get_session)):
    relacion = session.get(RutinaEjercicio, id)
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(relacion, key, value)
    session.add(relacion)
    session.commit()
    session.refresh(relacion)
    return {"mensaje": "Relación actualizada correctamente", "relacion": relacion}


@router.delete("/{id}")
def eliminar_relacion(id: int, session: Session = Depends(get_session)):
    relacion = session.get(RutinaEjercicio, id)
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    session.delete(relacion)
    session.commit()
    return {"mensaje": "Ejercicio eliminado de la rutina correctamente"}
