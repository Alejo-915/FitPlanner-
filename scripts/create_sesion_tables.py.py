from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import SesionEntrenamiento, EjercicioCompletado, Rutina, RutinaEjercicio, Ejercicio
from datetime import datetime
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/sesiones", tags=["Sesiones de Entrenamiento"])


# ============================================================
# MODELOS DE REQUEST
# ============================================================
class IniciarSesionRequest(BaseModel):
    usuario_id: int
    rutina_id: int


# ============================================================
# INICIAR SESIÓN DE ENTRENAMIENTO
# ============================================================
@router.post("/iniciar")
def iniciar_sesion(request: IniciarSesionRequest, session: Session = Depends(get_session)):
    """Inicia una nueva sesión de entrenamiento"""

    print(f"Iniciando sesión para usuario {request.usuario_id} y rutina {request.rutina_id}")

    # Verificar que la rutina existe
    rutina = session.get(Rutina, request.rutina_id)
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")

    # Verificar si hay sesión activa
    sesion_existente = session.exec(
        select(SesionEntrenamiento)
        .where(SesionEntrenamiento.usuario_id == request.usuario_id)
        .where(SesionEntrenamiento.completada == False)
    ).first()

    if sesion_existente:
        return {
            "mensaje": "Ya tienes una sesión activa",
            "sesion_id": sesion_existente.id,
            "rutina": rutina.nombre
        }

    # Crear nueva sesión
    nueva_sesion = SesionEntrenamiento(
        usuario_id=request.usuario_id,
        rutina_id=request.rutina_id,
        fecha_inicio=datetime.now(),
        completada=False
    )
    session.add(nueva_sesion)
    session.commit()
    session.refresh(nueva_sesion)

    print(f"Sesión creada con ID: {nueva_sesion.id}")

    # Obtener ejercicios de la rutina
    ejercicios_rutina = session.exec(
        select(RutinaEjercicio, Ejercicio)
        .where(RutinaEjercicio.rutina_id == request.rutina_id)
        .join(Ejercicio, Ejercicio.id == RutinaEjercicio.ejercicio_id)
    ).all()

    print(f"Ejercicios encontrados: {len(ejercicios_rutina)}")

    # Crear registros de ejercicios a completar
    for rutina_ej, ejercicio in ejercicios_rutina:
        ejercicio_completado = EjercicioCompletado(
            sesion_id=nueva_sesion.id,
            ejercicio_id=ejercicio.id,
            completado=False
        )
        session.add(ejercicio_completado)

    session.commit()

    return {
        "mensaje": "Sesión iniciada correctamente",
        "sesion_id": nueva_sesion.id,
        "rutina": rutina.nombre,
        "ejercicios_count": len(ejercicios_rutina)
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

    duracion_segundos = (sesion.fecha_fin - sesion.fecha_inicio).total_seconds()
    duracion_minutos = duracion_segundos / 60

    return {
        "mensaje": "¡Sesión completada exitosamente!",
        "duracion_minutos": round(duracion_minutos, 2)
    }


# ============================================================
# OBTENER SESIÓN ACTIVA
# ============================================================
@router.get("/usuario/{usuario_id}/activa")
def obtener_sesion_activa(usuario_id: int, session: Session = Depends(get_session)):
    """Obtiene la sesión activa de un usuario si existe"""

    print(f"Buscando sesión activa para usuario {usuario_id}")

    sesion_activa = session.exec(
        select(SesionEntrenamiento)
        .where(SesionEntrenamiento.usuario_id == usuario_id)
        .where(SesionEntrenamiento.completada == False)
    ).first()

    if not sesion_activa:
        print("No hay sesión activa")
        return {"sesion_id": None, "ejercicios": []}

    print(f"Sesión activa encontrada: {sesion_activa.id}")

    # Obtener la rutina
    rutina = session.get(Rutina, sesion_activa.rutina_id)

    # Obtener ejercicios de la sesión con detalles
    ejercicios = session.exec(
        select(EjercicioCompletado, Ejercicio, RutinaEjercicio)
        .where(EjercicioCompletado.sesion_id == sesion_activa.id)
        .join(Ejercicio, Ejercicio.id == EjercicioCompletado.ejercicio_id)
        .join(RutinaEjercicio,
              (RutinaEjercicio.ejercicio_id == Ejercicio.id) &
              (RutinaEjercicio.rutina_id == sesion_activa.rutina_id))
    ).all()

    print(f"Ejercicios en la sesión: {len(ejercicios)}")

    ejercicios_detalle = []
    for ej_comp, ejercicio, rutina_ej in ejercicios:
        ejercicios_detalle.append({
            "id_completado": ej_comp.id,
            "ejercicio_id": ejercicio.id,
            "nombre": ejercicio.nombre,
            "grupo_muscular": ejercicio.grupo_muscular,
            "video_url": ejercicio.video_url if ejercicio.video_url else "",
            "descripcion": ejercicio.descripcion,
            "series": rutina_ej.series,
            "repeticiones": rutina_ej.repeticiones,
            "completado": ej_comp.completado,
            "notas": ej_comp.notas if ej_comp.notas else ""
        })

    return {
        "sesion_id": sesion_activa.id,
        "rutina_id": sesion_activa.rutina_id,
        "rutina_nombre": rutina.nombre if rutina else "Sin nombre",
        "fecha_inicio": sesion_activa.fecha_inicio.isoformat(),
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

    historial = []
    for sesion, rutina in sesiones:
        duracion = 0
        if sesion.fecha_fin:
            duracion = (sesion.fecha_fin - sesion.fecha_inicio).total_seconds() / 60

        historial.append({
            "sesion_id": sesion.id,
            "rutina": rutina.nombre,
            "fecha": sesion.fecha_inicio.isoformat(),
            "duracion_minutos": round(duracion, 2)
        })

    return {"historial": historial}
