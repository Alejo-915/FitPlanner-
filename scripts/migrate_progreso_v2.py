"""
Script de migración para ampliar la tabla progreso con nuevos campos.
Ejecutar UNA sola vez:

    python scripts/migrate_progreso_v2.py
"""
from sqlalchemy import text
from db import engine

NUEVAS_COLUMNAS = [
    ("progreso", "cintura_cm",       "ALTER TABLE progreso ADD COLUMN cintura_cm REAL"),
    ("progreso", "porcentaje_grasa", "ALTER TABLE progreso ADD COLUMN porcentaje_grasa REAL"),
    ("progreso", "energia",          "ALTER TABLE progreso ADD COLUMN energia INTEGER DEFAULT 3"),
    ("progreso", "notas",            "ALTER TABLE progreso ADD COLUMN notas VARCHAR"),
]

def columna_existe(conn, tabla, columna):
    result = conn.execute(text(f"PRAGMA table_info({tabla})"))
    return any(row[1] == columna for row in result)

def migrar():
    print("🔄 Migrando tabla progreso...\n")
    with engine.begin() as conn:
        for tabla, columna, sql in NUEVAS_COLUMNAS:
            if columna_existe(conn, tabla, columna):
                print(f"ℹ️  {tabla}.{columna} ya existe")
            else:
                conn.execute(text(sql))
                print(f"✅ {tabla}.{columna} añadida")
    print("\n✅ Migración completada.")

if __name__ == "__main__":
    migrar()