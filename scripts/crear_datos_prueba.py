"""
Script para crear datos de prueba en la base de datos
"""
from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import Usuario, Ejercicio, Rutina, RutinaEjercicio


def crear_datos_prueba():
    print("🔧 Creando datos de prueba...\n")

    # 1. Asegurar que las tablas existen
    print("1️⃣ Creando tablas si no existen...")
    create_db_and_tables()
    print("   ✅ Tablas verificadas\n")

    with Session(engine) as session:
        # 2. Crear/Verificar Usuario
        print("2️⃣ Verificando usuario...")
        usuario = session.exec(select(Usuario).where(Usuario.id == 1)).first()

        if not usuario:
            print("   📝 Creando usuario de prueba...")
            usuario = Usuario(
                nombre="EDWIN pere",
                correo="edwinlm915@gmail.com",
                contraseña="edwin123",
                edad=13,
                peso=67.0,
                altura=190.0,
                objetivo="Perder peso",
                activo=True
            )
            session.add(usuario)
            session.commit()
            session.refresh(usuario)
            print(f"   ✅ Usuario creado: ID={usuario.id}\n")
        else:
            print(f"   ✅ Usuario ya existe: ID={usuario.id}\n")

        # 3. Crear Ejercicios
        print("3️⃣ Creando ejercicios...")
        ejercicios_data = [
            {
                "nombre": "Press Banca Plano",
                "grupo_muscular": "Pecho",
                "equipo": "Barra",
                "descripcion": "Ejercicio fundamental para desarrollo de pecho"
            },
            {
                "nombre": "Remo con Barra",
                "grupo_muscular": "Espalda",
                "equipo": "Barra",
                "descripcion": "Ejercicio para desarrollo de espalda media"
            },
            {
                "nombre": "Press Militar",
                "grupo_muscular": "Hombros",
                "equipo": "Barra",
                "descripcion": "Ejercicio compuesto para hombros"
            },
            {
                "nombre": "Sentadilla",
                "grupo_muscular": "Piernas",
                "equipo": "Barra",
                "descripcion": "Ejercicio fundamental para piernas"
            },
            {
                "nombre": "Peso Muerto",
                "grupo_muscular": "Espalda",
                "equipo": "Barra",
                "descripcion": "Ejercicio compuesto para espalda y piernas"
            }
        ]

        ejercicios_creados = []
        for ej_data in ejercicios_data:
            ej_existente = session.exec(
                select(Ejercicio).where(Ejercicio.nombre == ej_data["nombre"])
            ).first()

            if not ej_existente:
                ej = Ejercicio(**ej_data)
                session.add(ej)
                ejercicios_creados.append(ej_data["nombre"])

        session.commit()

        if ejercicios_creados:
            print(f"   ✅ {len(ejercicios_creados)} ejercicios creados")
        else:
            print("   ℹ️ Todos los ejercicios ya existen")
        print()

        # 4. Crear Rutinas
        print("4️⃣ Creando rutinas...")

        # Rutina 1: Hipertrofia y Fuerza
        rutina1 = session.exec(
            select(Rutina).where(Rutina.nombre == "Rutina de Hipertrofia y Fuerza")
        ).first()

        if not rutina1:
            rutina1 = Rutina(
                usuario_id=usuario.id,
                nombre="Rutina de Hipertrofia y Fuerza",
                nivel="Intermedio",
                frecuencia=3
            )
            session.add(rutina1)
            session.commit()
            session.refresh(rutina1)

            # Asignar ejercicios
            ejercicio1 = session.exec(select(Ejercicio).where(Ejercicio.nombre == "Press Banca Plano")).first()
            ejercicio2 = session.exec(select(Ejercicio).where(Ejercicio.nombre == "Remo con Barra")).first()
            ejercicio3 = session.exec(select(Ejercicio).where(Ejercicio.nombre == "Press Militar")).first()

            if ejercicio1:
                session.add(RutinaEjercicio(
                    rutina_id=rutina1.id,
                    ejercicio_id=ejercicio1.id,
                    series=4,
                    repeticiones=10,
                    duracion=45
                ))

            if ejercicio2:
                session.add(RutinaEjercicio(
                    rutina_id=rutina1.id,
                    ejercicio_id=ejercicio2.id,
                    series=4,
                    repeticiones=12,
                    duracion=40
                ))

            if ejercicio3:
                session.add(RutinaEjercicio(
                    rutina_id=rutina1.id,
                    ejercicio_id=ejercicio3.id,
                    series=3,
                    repeticiones=15,
                    duracion=35
                ))

            session.commit()
            print("   ✅ Rutina 'Hipertrofia y Fuerza' creada")
        else:
            print("   ℹ️ Rutina 'Hipertrofia y Fuerza' ya existe")

        # Rutina 2: Quema de Grasa HIIT
        rutina2 = session.exec(
            select(Rutina).where(Rutina.nombre == "Rutina Quema de Grasa HIIT")
        ).first()

        if not rutina2:
            rutina2 = Rutina(
                usuario_id=usuario.id,
                nombre="Rutina Quema de Grasa HIIT",
                nivel="Avanzado",
                frecuencia=4
            )
            session.add(rutina2)
            session.commit()
            session.refresh(rutina2)

            ejercicio4 = session.exec(select(Ejercicio).where(Ejercicio.nombre == "Sentadilla")).first()
            ejercicio5 = session.exec(select(Ejercicio).where(Ejercicio.nombre == "Peso Muerto")).first()
            ejercicio1 = session.exec(select(Ejercicio).where(Ejercicio.nombre == "Press Banca Plano")).first()

            if ejercicio4:
                session.add(RutinaEjercicio(
                    rutina_id=rutina2.id,
                    ejercicio_id=ejercicio4.id,
                    series=5,
                    repeticiones=8,
                    duracion=50
                ))

            if ejercicio5:
                session.add(RutinaEjercicio(
                    rutina_id=rutina2.id,
                    ejercicio_id=ejercicio5.id,
                    series=4,
                    repeticiones=6,
                    duracion=45
                ))

            if ejercicio1:
                session.add(RutinaEjercicio(
                    rutina_id=rutina2.id,
                    ejercicio_id=ejercicio1.id,
                    series=3,
                    repeticiones=12,
                    duracion=40
                ))

            session.commit()
            print("   ✅ Rutina 'Quema de Grasa HIIT' creada")
        else:
            print("   ℹ️ Rutina 'Quema de Grasa HIIT' ya existe")

        print()

        # Resumen
        print("=" * 60)
        print("✅ DATOS DE PRUEBA CREADOS")
        print("=" * 60)
        total_usuarios = len(session.exec(select(Usuario)).all())
        total_ejercicios = len(session.exec(select(Ejercicio)).all())
        total_rutinas = len(session.exec(select(Rutina)).all())
        total_relaciones = len(session.exec(select(RutinaEjercicio)).all())

        print(f"👤 Usuarios: {total_usuarios}")
        print(f"💪 Ejercicios: {total_ejercicios}")
        print(f"📋 Rutinas: {total_rutinas}")
        print(f"🔗 Ejercicios asignados: {total_relaciones}")
        print()
        print("🎯 Credenciales de prueba:")
        print("   Email: edwinlm915@gmail.com")
        print("   Contraseña: edwin123")
        print()
        print("🚀 Ahora puedes:")
        print("   1. Iniciar el servidor: uvicorn main:app --reload")
        print("   2. Ir a: http://127.0.0.1:8000/login")
        print("   3. Iniciar sesión con las credenciales de arriba")


if __name__ == "__main__":
    crear_datos_prueba()