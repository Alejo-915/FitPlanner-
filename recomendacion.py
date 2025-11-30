from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Recomendacion, Usuario

router = APIRouter(prefix="/recomendaciones", tags=["Recomendaciones"])

# ============================================================
# POST con IMC + objetivo personalizado
# ============================================================
@router.post("/")
def crear_recomendacion(rec: Recomendacion, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, rec.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Calcular IMC
    imc = usuario.peso / ((usuario.altura / 100) ** 2)
    rec.imc = round(imc, 2)

    # ---------------------------------------------------------
    # OBJETIVOS PERSONALIZADOS (lo que pediste)
    # ---------------------------------------------------------
    objetivo = usuario.objetivo.lower()

    if objetivo == "subir de peso":
        rec.descripcion = (
            "Objetivo: Subir de peso. Recomendación: dieta alta en calorías "
            "controladas, ejercicios de fuerza y progresión de cargas."
        )
    elif objetivo == "bajar de peso":
        rec.descripcion = (
            "Objetivo: Bajar de peso. Recomendación: déficit calórico moderado, "
            "cardio constante y entrenamiento funcional."
        )
    elif objetivo == "ganar masa muscular":
        rec.descripcion = (
            "Objetivo: Ganar masa muscular. Recomendación: rutina de fuerza, "
            "hipertrofia, volumen progresivo y adecuada ingesta de proteínas."
        )
    elif objetivo == "perder grasa":
        rec.descripcion = (
            "Objetivo: Perder grasa. Recomendación: combinar pesas con HIIT, "
            "control de calorías y buena hidratación."
        )
    elif objetivo == "mantener forma":
        rec.descripcion = (
            "Objetivo: Mantener forma. Recomendación: entrenamiento mixto, "
            "cardio ligero y fuerza para sostener un estado saludable."
        )
    else:
        rec.descripcion = (
            "Objetivo no reconocido. Ajusta el campo 'objetivo' para recibir una guía personalizada."
        )

    # Guardar recomendación
    session.add(rec)
    session.commit()
    session.refresh(rec)
    return rec

# ============================================================
# GET
# ============================================================
@router.get("/")
def listar_recomendaciones(session: Session = Depends(get_session)):
    return session.exec(select(Recomendacion)).all()

@router.get("/{usuario_id}")
def obtener_recomendacion(usuario_id: int, session: Session = Depends(get_session)):
    rec = session.exec(select(Recomendacion).where(Recomendacion.usuario_id == usuario_id)).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    return rec

# ============================================================
# PATCH
# ============================================================
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

# ============================================================
# DELETE
# ============================================================
@router.delete("/{id}")
def eliminar_recomendacion(id: int, session: Session = Depends(get_session)):
    rec = session.get(Recomendacion, id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    session.delete(rec)
    session.commit()
    return {"mensaje": "Recomendación eliminada correctamente"}
