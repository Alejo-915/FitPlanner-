from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Recomendacion, Usuario

router = APIRouter(prefix="/recomendaciones", tags=["Recomendaciones"])

@router.post("/")
def crear_recomendacion(rec: Recomendacion, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, rec.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    imc = usuario.peso / ((usuario.altura / 100) ** 2)
    rec.imc = round(imc, 2)
    if imc < 18.5:
        rec.descripcion = "Bajo peso: enfoca tu rutina en fuerza y ganancia muscular."
    elif imc <= 24.9:
        rec.descripcion = "Peso saludable: mantén equilibrio entre fuerza y resistencia."
    elif imc <= 29.9:
        rec.descripcion = "Sobrepeso: combina cardio con tonificación."
    else:
        rec.descripcion = "Obesidad: prioriza ejercicios de bajo impacto y nutrición."
    session.add(rec)
    session.commit()
    session.refresh(rec)
    return rec

@router.get("/")
def listar_recomendaciones(session: Session = Depends(get_session)):
    return session.exec(select(Recomendacion)).all()

@router.get("/{usuario_id}")
def obtener_recomendacion(usuario_id: int, session: Session = Depends(get_session)):
    rec = session.exec(select(Recomendacion).where(Recomendacion.usuario_id == usuario_id)).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    return rec

@router.patch("/{id}")
def actualizar_recomendacion(id: int, datos: Recomendacion, session: Session = Depends(get_session)):
    rec = session.get(Recomendacion, id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(rec, key, value)
    session.add(rec)
    session.commit()
    session.refresh(rec)
    return rec

@router.delete("/{id}")
def eliminar_recomendacion(id: int, session: Session = Depends(get_session)):
    rec = session.get(Recomendacion, id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    session.delete(rec)
    session.commit()
    return {"mensaje": "Recomendación eliminada correctamente"}
