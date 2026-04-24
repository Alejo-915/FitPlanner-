"""
Script para poblar la base de datos con ejercicios de ejemplo.
Ejecutar desde la raíz del proyecto:

    python scripts/seed_ejercicios.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from db import engine
from models import Ejercicio

EJERCICIOS = [
    # PECHO
    {"nombre": "Press de Banca Plano", "grupo_muscular": "Pecho", "equipo": "Barra", "dificultad": "moderado", "restricciones": "hombro", "descripcion": "Acostado en el banco, baja la barra al pecho y empuja hacia arriba manteniendo los codos a 45°.", "video_url": "https://www.youtube.com/watch?v=rT7DgCr-3pg"},
    {"nombre": "Press de Banca Inclinado", "grupo_muscular": "Pecho", "equipo": "Barra", "dificultad": "moderado", "restricciones": "hombro", "descripcion": "Igual que el press plano pero con el banco inclinado a 30-45°. Trabaja la parte superior del pecho.", "video_url": "https://www.youtube.com/watch?v=jPLdzuHckI8"},
    {"nombre": "Aperturas con Mancuernas", "grupo_muscular": "Pecho", "equipo": "Mancuernas", "dificultad": "fácil", "restricciones": "hombro", "descripcion": "Acostado, abre los brazos en arco hasta sentir el estiramiento en el pecho y regresa.", "video_url": "https://www.youtube.com/watch?v=eozdVDA78K0"},
    {"nombre": "Fondos en Paralelas", "grupo_muscular": "Pecho", "equipo": "Barras paralelas", "dificultad": "difícil", "restricciones": "hombro,muneca", "descripcion": "Apoyado en las barras, baja el cuerpo flexionando los codos y empuja hacia arriba.", "video_url": "https://www.youtube.com/watch?v=2z8JmcrW-As"},
    {"nombre": "Flexiones de Brazos", "grupo_muscular": "Pecho", "equipo": "Peso corporal", "dificultad": "fácil", "restricciones": "muneca", "descripcion": "En posición de plancha, baja el pecho al suelo y empuja hacia arriba.", "video_url": "https://www.youtube.com/watch?v=IODxDxX7oi4"},

    # ESPALDA
    {"nombre": "Peso Muerto", "grupo_muscular": "Espalda", "equipo": "Barra", "dificultad": "difícil", "restricciones": "espalda,rodilla", "descripcion": "Con la barra en el suelo, agáchate manteniendo la espalda recta y levanta el peso extendiendo caderas y rodillas.", "video_url": "https://www.youtube.com/watch?v=op9kVnSso6Q"},
    {"nombre": "Remo con Barra", "grupo_muscular": "Espalda", "equipo": "Barra", "dificultad": "moderado", "restricciones": "espalda", "descripcion": "Inclinado hacia adelante, lleva la barra hacia el abdomen apretando los omóplatos.", "video_url": "https://www.youtube.com/watch?v=FWJR5Ve8bnQ"},
    {"nombre": "Jalón al Pecho", "grupo_muscular": "Espalda", "equipo": "Polea", "dificultad": "fácil", "restricciones": None, "descripcion": "Sentado en la polea, jala la barra hacia el pecho manteniendo el torso ligeramente inclinado.", "video_url": "https://www.youtube.com/watch?v=CAwf7n6Luuc"},
    {"nombre": "Remo con Mancuerna", "grupo_muscular": "Espalda", "equipo": "Mancuernas", "dificultad": "fácil", "restricciones": "espalda", "descripcion": "Apoyado en el banco, jala la mancuerna hacia la cadera con un solo brazo.", "video_url": "https://www.youtube.com/watch?v=pYcpY20QaE8"},
    {"nombre": "Dominadas", "grupo_muscular": "Espalda", "equipo": "Barra fija", "dificultad": "difícil", "restricciones": "hombro,muneca", "descripcion": "Colgado de la barra, jala el cuerpo hacia arriba hasta que la barbilla supere la barra.", "video_url": "https://www.youtube.com/watch?v=eGo4IYlbE5g"},

    # PIERNAS
    {"nombre": "Sentadilla con Barra", "grupo_muscular": "Piernas", "equipo": "Barra", "dificultad": "moderado", "restricciones": "rodilla,espalda", "descripcion": "Con la barra en los trapecios, baja flexionando rodillas y caderas hasta 90° y regresa.", "video_url": "https://www.youtube.com/watch?v=ultWZbUMPL8"},
    {"nombre": "Prensa de Piernas", "grupo_muscular": "Piernas", "equipo": "Máquina", "dificultad": "fácil", "restricciones": "rodilla", "descripcion": "Sentado en la máquina, empuja la plataforma con los pies hasta extender las piernas.", "video_url": "https://www.youtube.com/watch?v=IZxyjW7MPJQ"},
    {"nombre": "Extensión de Cuádriceps", "grupo_muscular": "Piernas", "equipo": "Máquina", "dificultad": "fácil", "restricciones": "rodilla", "descripcion": "Sentado, extiende las piernas contra la resistencia de la máquina.", "video_url": "https://www.youtube.com/watch?v=YyvSfVjQeL0"},
    {"nombre": "Curl de Femoral", "grupo_muscular": "Piernas", "equipo": "Máquina", "dificultad": "fácil", "restricciones": "rodilla", "descripcion": "Boca abajo en la máquina, flexiona las rodillas llevando los talones hacia los glúteos.", "video_url": "https://www.youtube.com/watch?v=1Tq3QdYUuHs"},
    {"nombre": "Zancadas", "grupo_muscular": "Piernas", "equipo": "Mancuernas", "dificultad": "moderado", "restricciones": "rodilla,tobillo", "descripcion": "Da un paso largo al frente y baja la rodilla trasera casi al suelo. Alterna piernas.", "video_url": "https://www.youtube.com/watch?v=D7KaRcUTQeE"},
    {"nombre": "Elevación de Talones", "grupo_muscular": "Piernas", "equipo": "Peso corporal", "dificultad": "fácil", "restricciones": "tobillo", "descripcion": "De pie, sube en puntillas y baja lentamente para trabajar los gemelos.", "video_url": "https://www.youtube.com/watch?v=-M4-G8p1fCI"},

    # HOMBROS
    {"nombre": "Press Militar", "grupo_muscular": "Hombros", "equipo": "Barra", "dificultad": "moderado", "restricciones": "hombro,espalda", "descripcion": "De pie o sentado, empuja la barra desde los hombros hacia arriba hasta extender los brazos.", "video_url": "https://www.youtube.com/watch?v=2yjwXTZQDDI"},
    {"nombre": "Elevaciones Laterales", "grupo_muscular": "Hombros", "equipo": "Mancuernas", "dificultad": "fácil", "restricciones": "hombro", "descripcion": "Con mancuernas a los lados, eleva los brazos hasta la altura de los hombros.", "video_url": "https://www.youtube.com/watch?v=3VcKaXpzqRo"},
    {"nombre": "Elevaciones Frontales", "grupo_muscular": "Hombros", "equipo": "Mancuernas", "dificultad": "fácil", "restricciones": "hombro", "descripcion": "Eleva las mancuernas al frente hasta la altura de los hombros, alternando brazos.", "video_url": "https://www.youtube.com/watch?v=sOoBBCpgVeY"},
    {"nombre": "Pájaros", "grupo_muscular": "Hombros", "equipo": "Mancuernas", "dificultad": "fácil", "restricciones": "hombro", "descripcion": "Inclinado hacia adelante, abre los brazos en arco hacia atrás trabajando el deltoides posterior.", "video_url": "https://www.youtube.com/watch?v=6ZtPgUKCKmk"},

    # BRAZOS
    {"nombre": "Curl de Bíceps con Barra", "grupo_muscular": "Brazos", "equipo": "Barra", "dificultad": "fácil", "restricciones": "muneca", "descripcion": "De pie, flexiona los codos llevando la barra hacia los hombros sin mover los codos.", "video_url": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo"},
    {"nombre": "Curl Martillo", "grupo_muscular": "Brazos", "equipo": "Mancuernas", "dificultad": "fácil", "restricciones": "muneca", "descripcion": "Con agarre neutro (pulgares arriba), flexiona los codos llevando las mancuernas a los hombros.", "video_url": "https://www.youtube.com/watch?v=zC3nLlEvin4"},
    {"nombre": "Extensión de Tríceps en Polea", "grupo_muscular": "Brazos", "equipo": "Polea", "dificultad": "fácil", "restricciones": "muneca,codo", "descripcion": "De pie frente a la polea alta, extiende los codos empujando el cable hacia abajo.", "video_url": "https://www.youtube.com/watch?v=vB5OHsJ3EME"},
    {"nombre": "Press Francés", "grupo_muscular": "Brazos", "equipo": "Barra", "dificultad": "moderado", "restricciones": "muneca,codo", "descripcion": "Acostado, baja la barra hacia la frente flexionando solo los codos y extiende.", "video_url": "https://www.youtube.com/watch?v=d_KZxkY_0cM"},

    # CORE
    {"nombre": "Plancha Abdominal", "grupo_muscular": "Core", "equipo": "Peso corporal", "dificultad": "fácil", "restricciones": "muneca,espalda", "descripcion": "Apoyado en antebrazos y puntillas, mantén el cuerpo recto como una tabla.", "video_url": "https://www.youtube.com/watch?v=pSHjTRCQxIw"},
    {"nombre": "Crunch Abdominal", "grupo_muscular": "Core", "equipo": "Peso corporal", "dificultad": "fácil", "restricciones": "espalda,cuello", "descripcion": "Acostado boca arriba, eleva el torso hacia las rodillas contrayendo el abdomen.", "video_url": "https://www.youtube.com/watch?v=Xyd_fa5zoEU"},
    {"nombre": "Elevación de Piernas", "grupo_muscular": "Core", "equipo": "Peso corporal", "dificultad": "moderado", "restricciones": "espalda", "descripcion": "Acostado, eleva las piernas rectas hasta 90° y bájalas lentamente sin tocar el suelo.", "video_url": "https://www.youtube.com/watch?v=l4kQd9eWclE"},
    {"nombre": "Russian Twist", "grupo_muscular": "Core", "equipo": "Peso corporal", "dificultad": "fácil", "restricciones": "espalda", "descripcion": "Sentado con rodillas flexionadas, rota el torso de lado a lado sosteniendo un peso.", "video_url": "https://www.youtube.com/watch?v=wkD8rjkodUI"},
    {"nombre": "Plancha Lateral", "grupo_muscular": "Core", "equipo": "Peso corporal", "dificultad": "moderado", "restricciones": "muneca,hombro", "descripcion": "Apoyado en un antebrazo y el costado del pie, mantén el cuerpo recto.", "video_url": "https://www.youtube.com/watch?v=K2KACpntDX0"},

    # CARDIOVASCULAR
    {"nombre": "Trote en Cinta", "grupo_muscular": "Cardiovascular", "equipo": "Cinta de correr", "dificultad": "fácil", "restricciones": "rodilla,tobillo", "descripcion": "Trota a ritmo moderado (7-10 km/h) durante 20-30 minutos para trabajar el sistema cardiorrespiratorio.", "video_url": "https://www.youtube.com/watch?v=_kGESn8ArrU"},
    {"nombre": "Bicicleta Estática", "grupo_muscular": "Cardiovascular", "equipo": "Bicicleta estática", "dificultad": "fácil", "restricciones": "tobillo", "descripcion": "Pedalea a ritmo constante durante 20-40 minutos. Excelente para personas con problemas de rodilla.", "video_url": "https://www.youtube.com/watch?v=MgaGMSzKp4c"},
    {"nombre": "Saltar la Cuerda", "grupo_muscular": "Cardiovascular", "equipo": "Cuerda", "dificultad": "moderado", "restricciones": "rodilla,tobillo", "descripcion": "Salta la cuerda a ritmo constante. Mejora coordinación y resistencia cardiovascular.", "video_url": "https://www.youtube.com/watch?v=FJmRQ5iTXKE"},
    {"nombre": "Burpees", "grupo_muscular": "Full body", "equipo": "Peso corporal", "dificultad": "difícil", "restricciones": "rodilla,espalda,hombro,muneca", "descripcion": "Combina sentadilla, plancha, flexión y salto. Ejercicio de alta intensidad para quemar calorías.", "video_url": "https://www.youtube.com/watch?v=dZgVxmf6jkA"},
    {"nombre": "Mountain Climbers", "grupo_muscular": "Full body", "equipo": "Peso corporal", "dificultad": "moderado", "restricciones": "muneca,hombro", "descripcion": "En posición de plancha, lleva alternadamente las rodillas hacia el pecho a ritmo rápido.", "video_url": "https://www.youtube.com/watch?v=nmwgirgXLYM"},
]


def seed():
    print("🌱 Insertando ejercicios en la base de datos...\n")
    with Session(engine) as session:
        existentes = session.exec(select(Ejercicio)).all()
        nombres_existentes = {e.nombre for e in existentes}

        insertados = 0
        omitidos = 0

        for data in EJERCICIOS:
            if data["nombre"] in nombres_existentes:
                print(f"  ⏭️  Ya existe: {data['nombre']}")
                omitidos += 1
                continue

            ej = Ejercicio(
                nombre=data["nombre"],
                grupo_muscular=data["grupo_muscular"],
                equipo=data["equipo"],
                dificultad=data["dificultad"],
                restricciones=data["restricciones"],
                descripcion=data["descripcion"],
                video_url=data["video_url"],
            )
            session.add(ej)
            print(f"  ✅ {data['nombre']} ({data['grupo_muscular']})")
            insertados += 1

        session.commit()

    print(f"\n✅ Listo: {insertados} ejercicios insertados, {omitidos} omitidos.")
    print("👉 Abre http://127.0.0.1:8000/admin/ejercicios para verlos.")


if __name__ == "__main__":
    seed()