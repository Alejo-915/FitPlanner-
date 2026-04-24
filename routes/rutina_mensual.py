from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from db import get_session
from models import Rutina, Ejercicio, RutinaEjercicio, Usuario

router = APIRouter(prefix="/rutinas_mensuales", tags=["Rutinas Mensuales"])


NIVEL_SERIES = {
    "principiante": {"series": 2, "reps": 10, "carga_factor": 0.4},
    "intermedio":   {"series": 3, "reps": 12, "carga_factor": 0.6},
    "avanzado":     {"series": 4, "reps": 15, "carga_factor": 0.8},
}

# Progresión semanal: cada semana sube ligeramente la carga
PROGRESION_SEMANA = {1: 1.0, 2: 1.05, 3: 1.10, 4: 1.15}


def ejercicios_compatibles(ejercicios: list, limitaciones: list) -> list:
    """Filtra ejercicios que choquen con las limitaciones del usuario."""
    if not limitaciones:
        return ejercicios
    compatibles = []
    for ej in ejercicios:
        restricciones_ej = (
            [r.strip().lower() for r in ej.restricciones.split(",")]
            if ej.restricciones
            else []
        )
        conflicto = any(lim in restricciones_ej for lim in limitaciones)
        if not conflicto:
            compatibles.append(ej)
    return compatibles


@router.post("/generar/{usuario_id}")
def generar_rutina_mensual(
    usuario_id: int,
    mes: int = 1,
    anio: int = 2025,
    session: Session = Depends(get_session),
):
    """
    Genera automáticamente 4 semanas de rutinas para un usuario,
    respetando sus limitaciones físicas y progresando la carga semana a semana.
    """
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    limitaciones = (
        [l.strip().lower() for l in usuario.limitaciones.split(",")]
        if usuario.limitaciones
        else []
    )
    nivel = usuario.nivel_condicion or "principiante"
    dias = usuario.dias_semana or 3
    params = NIVEL_SERIES[nivel]

    # Obtener todos los ejercicios y filtrar por limitaciones
    todos = session.exec(select(Ejercicio)).all()
    compatibles = ejercicios_compatibles(todos, limitaciones)

    if not compatibles:
        raise HTTPException(
            status_code=400,
            detail="No hay ejercicios compatibles con las limitaciones del usuario."
        )

    rutinas_creadas = []

    for semana in range(1, 5):
        nombre_rutina = f"Rutina Semana {semana} - {mes}/{anio}"
        rutina = Rutina(
            usuario_id=usuario_id,
            nombre=nombre_rutina,
            nivel=nivel,
            frecuencia=dias,
            mes=mes,
            anio=anio,
        )
        session.add(rutina)
        session.commit()
        session.refresh(rutina)

        # Seleccionar ejercicios según días disponibles (rotar grupos musculares)
        grupos = list({ej.grupo_muscular for ej in compatibles})
        ejercicios_semana = compatibles[: dias * 3]  # ~3 ejercicios por día

        factor_semana = PROGRESION_SEMANA[semana]

        for ej in ejercicios_semana:
            re = RutinaEjercicio(
                rutina_id=rutina.id,
                ejercicio_id=ej.id,
                series=params["series"],
                repeticiones=params["reps"],
                duracion=45,
                semana=semana,
                carga_kg=round(params["carga_factor"] * factor_semana * 20, 1),
            )
            session.add(re)

        session.commit()
        rutinas_creadas.append({
            "semana": semana,
            "rutina_id": rutina.id,
            "nombre": nombre_rutina,
            "ejercicios": len(ejercicios_semana),
        })

    return {
        "mensaje": f"Rutina mensual generada para {usuario.nombre}",
        "nivel": nivel,
        "dias_semana": dias,
        "limitaciones_respetadas": limitaciones,
        "semanas": rutinas_creadas,
    }


@router.get("/usuario/{usuario_id}")
def rutinas_del_usuario(
    usuario_id: int,
    mes: int = None,
    anio: int = None,
    session: Session = Depends(get_session),
):
    """Lista rutinas de un usuario, opcionalmente filtrando por mes/año."""
    query = select(Rutina).where(Rutina.usuario_id == usuario_id)
    if mes:
        query = query.where(Rutina.mes == mes)
    if anio:
        query = query.where(Rutina.anio == anio)
    return session.exec(query).all()


@router.post("/solicitar_subida/{usuario_id}")
def solicitar_subida_nivel(usuario_id: int, session: Session = Depends(get_session)):
    """
    El usuario solicita subir de nivel. Se analiza su progreso
    y se actualiza si cumple los criterios.
    """
    from models import Progreso
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Criterio simple: al menos 8 progresos registrados
    progresos = session.exec(
        select(Progreso).where(Progreso.usuario_id == usuario_id)
    ).all()

    niveles = ["principiante", "intermedio", "avanzado"]
    nivel_actual = usuario.nivel_condicion or "principiante"
    idx = niveles.index(nivel_actual) if nivel_actual in niveles else 0

    if len(progresos) >= 8 and idx < len(niveles) - 1:
        nuevo_nivel = niveles[idx + 1]
        usuario.nivel_condicion = nuevo_nivel
        session.add(usuario)
        session.commit()
        return {
            "aprobado": True,
            "nivel_anterior": nivel_actual,
            "nuevo_nivel": nuevo_nivel,
            "mensaje": f"¡Felicidades! Subiste a nivel {nuevo_nivel}.",
        }
    elif idx == len(niveles) - 1:
        return {"aprobado": False, "mensaje": "Ya estás en el nivel máximo: avanzado."}
    else:
        return {
            "aprobado": False,
            "mensaje": f"Necesitas al menos 8 registros de progreso. Tienes {len(progresos)}.",
        }