"""
Script para configurar completamente la base de datos y datos de prueba
"""
from sqlmodel import SQLModel, Session, select
from database import engine, create_db_and_tables
from models import Usuario, Ejercicio, Rutina, RutinaEjercicio, SesionEntrenamiento
from datetime import datetime


def setup_database():
    print("🔧 Configurando base de datos...\n")

    # 1. Crear todas las tablas
    print("1️⃣ Creando tablas...")
    create_db_and_tables()
    print("   ✅ Tablas creadas\n")

    with Session(engine) as session:
        # 2. Verificar si ya existe el usuario de prueba
        print("2️⃣ Verificando usuario de prueba...")
        usuario = session.exec(select(Usuario).where(Usuario.id == 1)).first()

        if not usuario:
            print("   📝 Creando usuario de prueba...")
            usuario = Usuario(
                nombre="Juan Pérez",
                correo="juan@test.com",
                contraseña="test123",
                edad=28,
                peso=78.5,
                altura=175.0,
                objetivo="Ganar Músculo",
                activo=True
            )
            session.add(usuario)
            session.commit()
            session.refresh(usuario)
            print(f"   ✅ Usuario creado: ID={usuario.id}, Nombre={usuario.nombre}\n")
        else:
            print(f"   ✅ Usuario ya existe: ID={usuario.id}, Nombre={usuario.nombre}\n")

        # 3. Verificar ejercicios
        print("3️⃣ Verificando ejercicios...")
        ejercicios_count = len(session.exec(select(Ejercicio)).all())

        if ejercicios_count == 0:
            print("   📝 Creando ejercicios de prueba...")
            ejercicios = [
                Ejercicio(
                    nombre="Press Banca Plano",
                    grupo_muscular="Pecho",
                    equipo="Barra",
                    descripcion="Ejercicio fundamental para desarrollo de pecho",
                    video_url="https://www.youtube.com/watch?v=example1"
                ),
                Ejercicio(
                    nombre="Remo con Barra",
                    grupo_muscular="Espalda",
                    equipo="Barra",
                    descripcion="Ejercicio para desarrollo de espalda media",
                    video_url="https://www.youtube.com/watch?v=example2"
                ),
                Ejercicio(
                    nombre="Press Militar",
                    grupo_muscular="Hombros",
                    equipo="Barra",
                    descripcion="Ejercicio compuesto para hombros",
                    video_url="https://www.youtube.com/watch?v=example3"
                ),
                Ejercicio(
                    nombre="Sentadilla",
                    grupo_muscular="Piernas",
                    equipo="Barra",
                    descripcion="Ejercicio fundamental para desarrollo de piernas",
                    video_url="https://www.youtube.com/watch?v=example4"
                )
            ]

            for ej in ejercicios:
                session.add(ej)

            session.commit()
            print(f"   ✅ {len(ejercicios)} ejercicios creados\n")
        else:
            print(f"   ✅ Ya existen {ejercicios_count} ejercicios\n")

        # 4. Verificar rutinas
        print("4️⃣ Verificando rutinas...")
        rutinas = session.exec(select(Rutina).where(Rutina.usuario_id == usuario.id)).all()

        if len(rutinas) == 0:
            print("   📝 Creando rutinas de prueba...")

            # Rutina 1: Torso
            rutina_torso = Rutina(
                usuario_id=usuario.id,
                nombre="Torso / Hipertrofia",
                nivel="Intermedio",
                frecuencia=3
            )
            session.add(rutina_torso)
            session.commit()
            session.refresh(rutina_torso)

            # Obtener ejercicios
            ejercicio_press = session.exec(select(Ejercicio).where(Ejercicio.nombre == "Press Banca Plano")).first()
            ejercicio_remo = session.exec(select(Ejercicio).where(Ejercicio.nombre == "Remo con Barra")).first()
            ejercicio_militar = session.exec(select(Ejercicio).where(Ejercicio.nombre == "Press Militar")).first()

            # Asignar ejercicios a la rutina
            if ejercicio_press:
                rel1 = RutinaEjercicio(
                    rutina_id=rutina_torso.id,
                    ejercicio_id=ejercicio_press.id,
                    series=4,
                    repeticiones=10,
                    duracion=45
                )
                session.add(rel1)

            if ejercicio_remo:
                rel2 = RutinaEjercicio(
                    rutina_id=rutina_torso.id,
                    ejercicio_id=ejercicio_remo.id,
                    series=4,
                    repeticiones=12,
                    duracion=40
                )
                session.add(rel2)

            if ejercicio_militar:
                rel3 = RutinaEjercicio(
                    rutina_id=rutina_torso.id,
                    ejercicio_id=ejercicio_militar.id,
                    series=3,
                    repeticiones=15,
                    duracion=35
                )
                session.add(rel3)

            # Rutina 2: Piernas
            ejercicio_sentadilla = session.exec(select(Ejercicio).where(Ejercicio.nombre == "Sentadilla")).first()

            rutina_piernas = Rutina(
                usuario_id=usuario.id,
                nombre="Piernas / Fuerza",
                nivel="Intermedio",
                frecuencia=2
            )
            session.add(rutina_piernas)
            session.commit()
            session.refresh(rutina_piernas)

            if ejercicio_sentadilla:
                rel4 = RutinaEjercicio(
                    rutina_id=rutina_piernas.id,
                    ejercicio_id=ejercicio_sentadilla.id,
                    series=5,
                    repeticiones=8,
                    duracion=50
                )
                session.add(rel4)

            session.commit()
            print(f"   ✅ 2 rutinas creadas con sus ejercicios\n")
        else:
            print(f"   ✅ Ya existen {len(rutinas)} rutinas\n")

        # 5. Resumen final
        print("=" * 50)
        print("✅ CONFIGURACIÓN COMPLETA")
        print("=" * 50)
        print(f"👤 Usuarios: {len(session.exec(select(Usuario)).all())}")
        print(f"💪 Ejercicios: {len(session.exec(select(Ejercicio)).all())}")
        print(f"📋 Rutinas: {len(session.exec(select(Rutina)).all())}")
        print(f"🔗 Relaciones Rutina-Ejercicio: {len(session.exec(select(RutinaEjercicio)).all())}")
        print("\n🚀 Ahora puedes iniciar el servidor con: uvicorn main:app --reload")
        print("🌐 Y acceder a: http://127.0.0.1:8000/home/user")


if __name__ == "__main__":
    setup_database()