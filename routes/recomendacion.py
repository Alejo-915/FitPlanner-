from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Recomendacion, Usuario

router = APIRouter(prefix="/recomendaciones", tags=["Recomendaciones"])


def calcular_fase(imc: float, objetivo: str) -> str:
    """
    Determina qué debería hacer primero el usuario
    según su IMC y objetivo declarado.
    """
    objetivo = objetivo.lower()

    # Regla: si está en obesidad, primero perder peso sin importar el objetivo
    if imc >= 30:
        return "primero_perder_peso"

    # Bajo peso: no puede perder más peso
    if imc < 18.5:
        if "bajar" in objetivo or "perder" in objetivo:
            return "no_apto_perder_peso"
        return "primero_ganar_peso"

    # Sobrepeso moderado
    if imc >= 25:
        if "ganar" in objetivo or "masa" in objetivo or "músculo" in objetivo:
            return "primero_perder_grasa_luego_musculo"
        return "perder_grasa"

    # Peso saludable
    if "ganar" in objetivo or "masa" in objetivo or "músculo" in objetivo:
        return "ganar_musculo"
    if "bajar" in objetivo or "perder" in objetivo:
        return "perder_grasa_leve"
    return "mantener_forma"


def descripcion_por_fase(fase: str, limitaciones: list) -> str:
    base = {
        "primero_perder_peso": (
            "Dado tu IMC actual debes enfocarte PRIMERO en bajar de peso "
            "antes de trabajar en masa muscular. Prioriza cardio de bajo impacto "
            "y un déficit calórico moderado."
        ),
        "no_apto_perder_peso": (
            "⚠️ Tu IMC indica bajo peso. No es recomendable hacer un plan para "
            "perder peso. Te redirigimos a un plan de ganancia saludable de masa."
        ),
        "primero_ganar_peso": (
            "Tu peso actual está por debajo del rango saludable. "
            "Enfócate en aumentar calorías de calidad y ejercicios de fuerza "
            "para ganar masa muscular y peso corporal."
        ),
        "primero_perder_grasa_luego_musculo": (
            "Tienes sobrepeso. Te recomendamos primero un ciclo de pérdida de grasa "
            "(4-8 semanas de cardio + fuerza) y luego pasar a un plan de volumen muscular."
        ),
        "perder_grasa": (
            "Combina cardio constante con entrenamiento funcional. "
            "Mantén un déficit calórico moderado y buena hidratación."
        ),
        "ganar_musculo": (
            "Tu peso es saludable. Puedes enfocarte directamente en ganar masa muscular "
            "con rutinas de fuerza e hipertrofia, volumen progresivo y alta ingesta de proteínas."
        ),
        "perder_grasa_leve": (
            "Tu peso está en rango saludable. Un plan mixto de cardio ligero y fuerza "
            "te ayudará a definir sin perder masa muscular."
        ),
        "mantener_forma": (
            "Excelente condición. Mantén con entrenamiento mixto, cardio ligero "
            "y fuerza para sostener un estado óptimo."
        ),
    }

    desc = base.get(fase, "Consulta con un profesional para una guía personalizada.")

    # Agregar advertencias por limitaciones físicas
    avisos = {
        "rodilla": "⚠️ Rodilla: evita sentadillas profundas, saltos y carrera en superficies duras.",
        "espalda": "⚠️ Espalda: evita peso muerto convencional y movimientos de alto impacto espinal.",
        "hombro": "⚠️ Hombro: evita press militar pesado y jalones tras la nuca.",
        "cadera": "⚠️ Cadera: evita movimientos de alta rotación y sentadilla sumo pesada.",
        "muneca": "⚠️ Muñeca: prefiere mancuernas con agarre neutro y evita apoyos en extensión.",
        "tobillo": "⚠️ Tobillo: evita sentadillas profundas y ejercicios de salto.",
    }

    if limitaciones:
        desc += "\n\nConsideraciones por tus limitaciones físicas:"
        for lim in limitaciones:
            if lim in avisos:
                desc += f"\n{avisos[lim]}"

    return desc


# ─────────────────────────────────────────────────────────
@router.post("/")
def crear_recomendacion(rec: Recomendacion, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, rec.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not usuario.peso or not usuario.altura:
        raise HTTPException(
            status_code=400,
            detail="El usuario debe tener peso y altura registrados para generar recomendación."
        )

    imc = usuario.peso / ((usuario.altura / 100) ** 2)
    rec.imc = round(imc, 2)

    limitaciones = (
        [l.strip() for l in usuario.limitaciones.split(",")]
        if usuario.limitaciones
        else []
    )

    fase = calcular_fase(imc, usuario.objetivo)
    rec.fase_recomendada = fase
    rec.descripcion = descripcion_por_fase(fase, limitaciones)

    session.add(rec)
    session.commit()
    session.refresh(rec)
    return rec


@router.get("/")
def listar_recomendaciones(session: Session = Depends(get_session)):
    return session.exec(select(Recomendacion)).all()


@router.get("/{usuario_id}")
def obtener_recomendacion(usuario_id: int, session: Session = Depends(get_session)):
    rec = session.exec(
        select(Recomendacion).where(Recomendacion.usuario_id == usuario_id)
    ).first()
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