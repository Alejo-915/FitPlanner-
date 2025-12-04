from sqlalchemy import text, inspect
from database import engine


def verify_tables():
    """Verifica que todas las tablas necesarias existan"""

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print("📋 Tablas en la base de datos:")
    for table in sorted(tables):
        print(f"  ✓ {table}")

    required_tables = [
        'sesionentrenamiento',
        'ejerciciocompletado',
        'usuario',
        'ejercicio',
        'rutina',
        'rutinaejercicio'
    ]

    missing = []
    for table in required_tables:
        if table not in tables:
            missing.append(table)

    if missing:
        print("\n❌ Tablas faltantes:")
        for table in missing:
            print(f"  ✗ {table}")
        print("\n⚠️  Ejecuta: python scripts/create_sesion_tables.py")
    else:
        print("\n✅ Todas las tablas necesarias están presentes")


if __name__ == "__main__":
    verify_tables()
