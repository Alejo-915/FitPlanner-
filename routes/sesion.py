from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import SesionEntrenamiento, EjercicioCompletado, Rutina, RutinaEjercicio
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/sesiones", tags=["Sesiones"])


class IniciarSesionRequest(BaseModel):
    usuario_id: int
    rutina_id: int


class CompletarEjercicioRequest(BaseModel):
    ejercicio_id: int


@router.post("/iniciar")
def iniciar_sesion(data: IniciarSesionRequest, session: Session = Depends(get_session)):
    """Inicia una nueva sesión de entrenamiento"""
    try:
        # Verificar que la rutina existe
        rutina = session.get(Rutina, data.rutina_id)
        if not rutina:
            raise HTTPException(status_code=404, detail="Rutina no encontrada")

        # Verificar si ya hay una sesión activa
        sesion_activa = session.exec(
            select(SesionEntrenamiento)
            .where(SesionEntrenamiento.usuario_id == data.usuario_id)
            .where(SesionEntrenamiento.completada == False)
        ).first()

        if sesion_activa:
            raise HTTPException(status_code=400, detail="Ya tienes una sesión activa")

        # Crear nueva sesión
        nueva_sesion = SesionEntrenamiento(
            usuario_id=data.usuario_id,
            rutina_id=data.rutina_id,
            fecha_inicio=datetime.now(),
            completada=False
        )
        session.add(nueva_sesion)
        session.commit()
        session.refresh(nueva_sesion)

        # Obtener ejercicios de la rutina
        ejercicios = session.exec(
            select(RutinaEjercicio)
            .where(RutinaEjercicio.rutina_id == data.rutina_id)
        ).all()

        # Crear registros de ejercicios a completar
        for ejercicio_rutina in ejercicios:
            ejercicio_comp = EjercicioCompletado(
                sesion_id=nueva_sesion.id,
                ejercicio_id=ejercicio_rutina.ejercicio_id,
                series_completadas=0,
                completado=False
            )
            session.add(ejercicio_comp)

        session.commit()

        return {
            "message": "Sesión iniciada correctamente",
            "sesion_id": nueva_sesion.id,
            "rutina_id": data.rutina_id,
            "total_ejercicios": len(ejercicios)
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al iniciar sesión: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al iniciar sesión: {str(e)}")


@router.get("/usuario/{usuario_id}/activa")
def obtener_sesion_activa(usuario_id: int, session: Session = Depends(get_session)):
    """Obtiene la sesión activa de un usuario"""
    sesion = session.exec(
        select(SesionEntrenamiento)
        .where(SesionEntrenamiento.usuario_id == usuario_id)
        .where(SesionEntrenamiento.completada == False)
    ).first()

    if not sesion:
        return {"sesion_activa": False}

    # Obtener ejercicios completados
    ejercicios = session.exec(
        select(EjercicioCompletado)
        .where(EjercicioCompletado.sesion_id == sesion.id)
    ).all()

    return {
        "sesion_activa": True,
        "sesion_id": sesion.id,
        "rutina_id": sesion.rutina_id,
        "ejercicios": [
            {
                "ejercicio_id": ej.ejercicio_id,
                "completado": ej.completado,
                "series_completadas": ej.series_completadas
            }
            for ej in ejercicios
        ]
    }


@router.post("/{sesion_id}/completar-ejercicio")
def completar_ejercicio(
        sesion_id: int,
        data: CompletarEjercicioRequest,
        session: Session = Depends(get_session)
):
    """Marca un ejercicio como completado"""
    ejercicio = session.exec(
        select(EjercicioCompletado)
        .where(EjercicioCompletado.sesion_id == sesion_id)
        .where(EjercicioCompletado.ejercicio_id == data.ejercicio_id)
    ).first()

    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado en esta sesión")

    ejercicio.completado = True
    session.add(ejercicio)
    session.commit()

    return {"message": "Ejercicio completado", "ejercicio_id": data.ejercicio_id}


@router.post("/{sesion_id}/finalizar")
def finalizar_sesion(sesion_id: int, session: Session = Depends(get_session)):
    """Finaliza una sesión de entrenamiento"""
    sesion = session.get(SesionEntrenamiento, sesion_id)
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    sesion.completada = True
    sesion.fecha_fin = datetime.now()
    session.add(sesion)
    session.commit()

    return {"message": "Sesión finalizada correctamente", "sesion_id": sesion_id}
