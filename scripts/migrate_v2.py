"""
Script de migración para añadir las nuevas columnas al proyecto FitPlanner v2.
Ejecutar UNA sola vez sobre la base de datos existente:

    python scripts/migrate_v2.py
"""
from sqlalchemy import text
from db import engine


MIGRACIONES = [
    # Tabla usuario
    ("usuario", "limitaciones",          "ALTER TABLE usuario ADD COLUMN limitaciones VARCHAR"),
    ("usuario", "meses_sin_ejercicio",   "ALTER TABLE usuario ADD COLUMN meses_sin_ejercicio INTEGER DEFAULT 0"),
    ("usuario", "dias_semana",           "ALTER TABLE usuario ADD COLUMN dias_semana INTEGER DEFAULT 3"),
    ("usuario", "nivel_condicion",       "ALTER TABLE usuario ADD COLUMN nivel_condicion VARCHAR DEFAULT 'principiante'"),
    ("usuario", "fecha_evaluacion",      "ALTER TABLE usuario ADD COLUMN fecha_evaluacion DATE"),

    # Tabla ejercicio
    ("ejercicio", "dificultad",          "ALTER TABLE ejercicio ADD COLUMN dificultad VARCHAR DEFAULT 'moderado'"),
    ("ejercicio", "restricciones",       "ALTER TABLE ejercicio ADD COLUMN restricciones VARCHAR"),

    # Tabla rutina
    ("rutina", "mes",                    "ALTER TABLE rutina ADD COLUMN mes INTEGER DEFAULT 1"),
    ("rutina", "anio",                   "ALTER TABLE rutina ADD COLUMN anio INTEGER DEFAULT 2025"),

    # Tabla rutinaejercicio
    ("rutinaejercicio", "semana",        "ALTER TABLE rutinaejercicio ADD COLUMN semana INTEGER DEFAULT 1"),
    ("rutinaejercicio", "carga_kg",      "ALTER TABLE rutinaejercicio ADD COLUMN carga_kg REAL DEFAULT 0.0"),

    # Tabla progreso
    ("progreso", "imc_actual",           "ALTER TABLE progreso ADD COLUMN imc_actual REAL"),
    ("progreso", "nivel_solicitado",     "ALTER TABLE progreso ADD COLUMN nivel_solicitado VARCHAR"),

    # Tabla recomendacion
    ("recomendacion", "fase_recomendada","ALTER TABLE recomendacion ADD COLUMN fase_recomendada VARCHAR"),
]


def columna_existe(conn, tabla: str, columna: str) -> bool:
    result = conn.execute(text(f"PRAGMA table_info({tabla})"))
    return any(row[1] == columna for row in result)


def tabla_existe(conn, tabla: str) -> bool:
    result = conn.execute(
        text("SELECT name FROM sqlite_master WHERE type='table' AND name=:t"),
        {"t": tabla},
    )
    return result.first() is not None


def ejecutar_migraciones():
    print("🔄 Iniciando migración FitPlanner v2...\n")
    with engine.begin() as conn:
        # Crear tabla asistencia si no existe
        if not tabla_existe(conn, "asistencia"):
            conn.execute(text("""
                CREATE TABLE asistencia (
                    id INTEGER PRIMARY KEY,
                    usuario_id INTEGER NOT NULL REFERENCES usuario(id),
                    fecha DATE NOT NULL,
                    duracion_minutos INTEGER,
                    completada BOOLEAN NOT NULL DEFAULT 1
                )
            """))
            print("✅ Tabla 'asistencia' creada")
        else:
            print("ℹ️  Tabla 'asistencia' ya existe")

        # Añadir columnas a tablas existentes
        for tabla, columna, sql in MIGRACIONES:
            if not tabla_existe(conn, tabla):
                print(f"⚠️  Tabla '{tabla}' no existe, saltando columna '{columna}'")
                continue
            if columna_existe(conn, tabla, columna):
                print(f"ℹ️  {tabla}.{columna} ya existe")
            else:
                conn.execute(text(sql))
                print(f"✅ {tabla}.{columna} añadida")

    print("\n✅ Migración completada correctamente.")


if __name__ == "__main__":
    ejecutar_migraciones()