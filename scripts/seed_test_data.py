from sqlmodel import Session, select
from database import engine
from models import Usuario, Ejercicio, Rutina, RutinaEjercicio


def seed_test_data():
    """Crea datos de prueba si no existen"""

    with Session(engine) as session:
        print("🌱 Sembrando datos de prueba...\n")

        # Verificar/crear usuario de prueba
        usuario = session.get(Usuario, 1)
        if not usuario:
            print("Creando usuario de prueba...")
            usuario = Usuario(
                nombre="Carlos Mendoza",
                correo="carlos@test.com",
                contraseña="test123",
                edad=28,
                peso=78.5,
                altura=1.78,
                objetivo="Ganar masa muscular",
                activo=True
            )
            session.add(usuario)
            session.commit()
            session.refresh(usuario)
            print(f"✅ Usuario creado: ID {usuario.id}")
        else:
            print(f"ℹ️  Usuario ya existe: {usuario.nombre}")

        # Verificar/crear ejercicios de prueba
        ejercicios_data = [
            {
                "nombre": "Press de Banca",
                "grupo_muscular": "Pecho",
                "equipo": "Barra y banco",
                "descripcion": "Ejercicio compuesto para pecho, hombros y tríceps",
                "video_url": "https://www.youtube.com/watch?v=rT7DgCr-3pg"
            },
            {
                "nombre": "Sentadilla",
                "grupo_muscular": "Piernas",
                "equipo": "Barra",
                "descripcion": "Ejercicio fundamental para piernas y core",
                "video_url": "https://www.youtube.com/watch?v=ultWZbUMPL8"
            },
            {
                "nombre": "Peso Muerto",
                "grupo_muscular": "Espalda",
                "equipo": "Barra",
                "descripcion": "Ejercicio compuesto para espalda baja y piernas",
                "video_url": "https://www.youtube.com/watch?v=op9kVnSso6Q"
            }
        ]

        ejercicios_ids = []
        for ej_data in ejercicios_data:
            ejercicio = session.exec(
                select(Ejercicio).where(Ejercicio.nombre == ej_data["nombre"])
            ).first()

            if not ejercicio:
                ejercicio = Ejercicio(**ej_data)
                session.add(ejercicio)
                session.commit()
                session.refresh(ejercicio)
                print(f"✅ Ejercicio creado: {ejercicio.nombre}")
            else:
                print(f"ℹ️  Ejercicio ya existe: {ejercicio.nombre}")

            ejercicios_ids.append(ejercicio.id)

        # Verificar/crear rutina de prueba
        rutina = session.exec(
            select(Rutina).where(Rutina.nombre == "Rutina de Fuerza Básica")
        ).first()

        if not rutina:
            print("\nCreando rutina de prueba...")
            rutina = Rutina(
                usuario_id=usuario.id,
                nombre="Rutina de Fuerza Básica",
                nivel="Intermedio",
                frecuencia=3
            )
            session.add(rutina)
            session.commit()
            session.refresh(rutina)
            print(f"✅ Rutina creada: ID {rutina.id}")

            # Asignar ejercicios a la rutina
            print("\nAsignando ejercicios a la rutina...")
            parametros = [
                {"series": 4, "repeticiones": 8, "duracion": 30},
                {"series": 4, "repeticiones": 10, "duracion": 35},
                {"series": 3, "repeticiones": 6, "duracion": 25}
            ]

            for ej_id, params in zip(ejercicios_ids, parametros):
                rutina_ej = RutinaEjercicio(
                    rutina_id=rutina.id,
                    ejercicio_id=ej_id,
                    series=params["series"],
                    repeticiones=params["repeticiones"],
                    duracion=params["duracion"]
                )
                session.add(rutina_ej)

            session.commit()
            print("✅ Ejercicios asignados a la rutina")
        else:
            print(f"\nℹ️  Rutina ya existe: {rutina.nombre}")

        print("\n✅ Datos de prueba listos!")
        print(f"\n📊 Resumen:")
        print(f"   Usuario ID: {usuario.id} - {usuario.nombre}")
        print(f"   Ejercicios: {len(ejercicios_ids)}")
        print(f"   Rutina ID: {rutina.id} - {rutina.nombre}")


if __name__ == "__main__":
    seed_test_data()
