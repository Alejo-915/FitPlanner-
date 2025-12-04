from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import SesionEntrenamiento, EjercicioCompletado, Rutina, RutinaEjercicio, Ejercicio
from datetime import datetime
from typing import List

router = APIRouter(prefix="/sesiones", tags=["Sesiones de Entrenamiento"])


# ============================================================
# INICIAR SESIÓN DE ENTRENAMIENTO
# ============================================================
@router.post("/iniciar")
def iniciar_sesion(usuario_id: int, rutina_id: int, session: Session = Depends(get_session)):
    """Inicia una nueva sesión de entrenamiento"""

    # Verificar que la rutina existe
    rutina = session.get(Rutina, rutina_id)
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")

    # Crear nueva sesión
    nueva_sesion = SesionEntrenamiento(
        usuario_id=usuario_id,
        rutina_id=rutina_id,
        fecha_inicio=datetime.now(),
        completada=False
    )
    session.add(nueva_sesion)
    session.commit()
    session.refresh(nueva_sesion)

    # Obtener ejercicios de la rutina
    ejercicios_rutina = session.exec(
        select(RutinaEjercicio, Ejercicio)
        .where(RutinaEjercicio.rutina_id == rutina_id)
        .join(Ejercicio, Ejercicio.id == RutinaEjercicio.ejercicio_id)
    ).all()

    # Crear registros de ejercicios a completar
    for rutina_ej, ejercicio in ejercicios_rutina:
        ejercicio_completado = EjercicioCompletado(
            sesion_id=nueva_sesion.id,
            ejercicio_id=ejercicio.id,
            completado=False
        )
        session.add(ejercicio_completado)

    session.commit()
    session.refresh(nueva_sesion)

    return {
        "mensaje": "Sesión iniciada correctamente",
        "sesion_id": nueva_sesion.id,
        "rutina": rutina.nombre
    }


# ============================================================
# MARCAR EJERCICIO COMO COMPLETADO
# ============================================================
@router.patch("/ejercicio/{ejercicio_completado_id}/completar")
def marcar_ejercicio_completado(
        ejercicio_completado_id: int,
        completado: bool,
        notas: str = None,
        session: Session = Depends(get_session)
):
    """Marca un ejercicio como completado o no completado"""

    ejercicio = session.get(EjercicioCompletado, ejercicio_completado_id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    ejercicio.completado = completado
    if notas:
        ejercicio.notas = notas

    session.add(ejercicio)
    session.commit()
    session.refresh(ejercicio)

    return {
        "mensaje": "Ejercicio actualizado",
        "ejercicio_id": ejercicio.ejercicio_id,
        "completado": ejercicio.completado
    }


# ============================================================
# FINALIZAR SESIÓN
# ============================================================
@router.post("/{sesion_id}/finalizar")
def finalizar_sesion(sesion_id: int, session: Session = Depends(get_session)):
    """Finaliza una sesión de entrenamiento"""

    sesion = session.get(SesionEntrenamiento, sesion_id)
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    sesion.fecha_fin = datetime.now()
    sesion.completada = True

    session.add(sesion)
    session.commit()
    session.refresh(sesion)

    return {
        "mensaje": "¡Sesión completada exitosamente!",
        "duracion_minutos": (sesion.fecha_fin - sesion.fecha_inicio).total_seconds() / 60
    }


# ============================================================
# OBTENER SESIÓN ACTIVA
# ============================================================
@router.get("/usuario/{usuario_id}/activa")
def obtener_sesion_activa(usuario_id: int, session: Session = Depends(get_session)):
    """Obtiene la sesión activa de un usuario si existe"""

    sesion_activa = session.exec(
        select(SesionEntrenamiento)
        .where(SesionEntrenamiento.usuario_id == usuario_id)
        .where(SesionEntrenamiento.completada == False)
    ).first()

    if not sesion_activa:
        return {"sesion_activa": None}

    # Obtener ejercicios de la sesión con detalles
    ejercicios = session.exec(
        select(EjercicioCompletado, Ejercicio, RutinaEjercicio)
        .where(EjercicioCompletado.sesion_id == sesion_activa.id)
        .join(Ejercicio, Ejercicio.id == EjercicioCompletado.ejercicio_id)
        .join(RutinaEjercicio,
              (RutinaEjercicio.ejercicio_id == Ejercicio.id) &
              (RutinaEjercicio.rutina_id == sesion_activa.rutina_id))
    ).all()

    ejercicios_detalle = [
        {
            "id_completado": ej_comp.id,
            "ejercicio_id": ejercicio.id,
            "nombre": ejercicio.nombre,
            "grupo_muscular": ejercicio.grupo_muscular,
            "video_url": ejercicio.video_url,
            "descripcion": ejercicio.descripcion,
            "series": rutina_ej.series,
            "repeticiones": rutina_ej.repeticiones,
            "completado": ej_comp.completado,
            "notas": ej_comp.notas
        }
        for ej_comp, ejercicio, rutina_ej in ejercicios
    ]

    return {
        "sesion_id": sesion_activa.id,
        "rutina_id": sesion_activa.rutina_id,
        "fecha_inicio": sesion_activa.fecha_inicio,
        "ejercicios": ejercicios_detalle
    }


# ============================================================
# HISTORIAL DE SESIONES
# ============================================================
@router.get("/usuario/{usuario_id}/historial")
def obtener_historial_sesiones(usuario_id: int, session: Session = Depends(get_session)):
    """Obtiene el historial de sesiones completadas de un usuario"""

    sesiones = session.exec(
        select(SesionEntrenamiento, Rutina)
        .where(SesionEntrenamiento.usuario_id == usuario_id)
        .where(SesionEntrenamiento.completada == True)
        .join(Rutina, Rutina.id == SesionEntrenamiento.rutina_id)
        .order_by(SesionEntrenamiento.fecha_inicio.desc())
    ).all()

    historial = [
        {
            "sesion_id": sesion.id,
            "rutina": rutina.nombre,
            "fecha": sesion.fecha_inicio,
            "duracion_minutos": (sesion.fecha_fin - sesion.fecha_inicio).total_seconds() / 60 if sesion.fecha_fin else 0
        }
        for sesion, rutina in sesiones
    ]

    return {"historial": historial}
