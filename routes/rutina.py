from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Rutina, RutinaEjercicio, Ejercicio

router = APIRouter(prefix="/rutinas", tags=["Rutinas"])

# ✅ Crear una nueva rutina
@router.post("/")
def crear_rutina(rutina: Rutina, session: Session = Depends(get_session)):
    if not rutina.nombre or not rutina.usuario_id:
        raise HTTPException(status_code=400, detail="Debe incluir nombre y usuario_id")

    session.add(rutina)
    session.commit()
    session.refresh(rutina)
    return {
        "mensaje": "Rutina creada exitosamente",
        "rutina": rutina
    }


# ✅ Listar todas las rutinas con sus ejercicios y parámetros
@router.get("/")
def listar_rutinas_con_ejercicios(session: Session = Depends(get_session)):
    rutinas = session.exec(select(Rutina)).all()
    if not rutinas:
        raise HTTPException(status_code=404, detail="No hay rutinas registradas")

    resultado = []
    for rutina in rutinas:
        relaciones = session.exec(
            select(RutinaEjercicio, Ejercicio)
            .where(RutinaEjercicio.rutina_id == rutina.id)
            .join(Ejercicio, Ejercicio.id == RutinaEjercicio.ejercicio_id)
        ).all()

        ejercicios_info = [
            {
                "id": ej.id,
                "nombre": ej.nombre,
                "grupo_muscular": ej.grupo_muscular,
                "series": re.series,
                "repeticiones": re.repeticiones,
                "duracion": re.duracion
            }
            for re, ej in relaciones
        ]

        resultado.append({
            "id": rutina.id,
            "nombre_rutina": rutina.nombre,
            "nivel": rutina.nivel,
            "frecuencia": rutina.frecuencia,
            "usuario_id": rutina.usuario_id,
            "ejercicios": ejercicios_info
        })

    return {"rutinas": resultado}


# ✅ Consultar una rutina específica con sus ejercicios
@router.get("/{rutina_id}")
def obtener_rutina_por_id(rutina_id: int, session: Session = Depends(get_session)):
    rutina = session.get(Rutina, rutina_id)
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")

    relaciones = session.exec(
        select(RutinaEjercicio, Ejercicio)
        .where(RutinaEjercicio.rutina_id == rutina.id)
        .join(Ejercicio, Ejercicio.id == RutinaEjercicio.ejercicio_id)
    ).all()

    ejercicios_info = [
        {
            "id": ej.id,
            "nombre": ej.nombre,
            "grupo_muscular": ej.grupo_muscular,
            "series": re.series,
            "repeticiones": re.repeticiones,
            "duracion": re.duracion
        }
        for re, ej in relaciones
    ]

    return {
        "id": rutina.id,
        "nombre_rutina": rutina.nombre,
        "nivel": rutina.nivel,
        "frecuencia": rutina.frecuencia,
        "usuario_id": rutina.usuario_id,
        "ejercicios": ejercicios_info
    }

@router.patch("/{id}")
def actualizar_rutina(id: int, datos: Rutina, session: Session = Depends(get_session)):
    rutina = session.get(Rutina, id)
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(rutina, key, value)
    session.add(rutina)
    session.commit()
    session.refresh(rutina)
    return rutina

@router.delete("/{id}")
def eliminar_rutina(id: int, session: Session = Depends(get_session)):
    rutina = session.get(Rutina, id)
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    session.delete(rutina)
    session.commit()
    return {"mensaje": "Rutina eliminada correctamente"}
