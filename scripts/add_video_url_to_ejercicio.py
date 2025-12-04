from sqlalchemy import text
from db import engine


def add_video_url_column():
    """Agregar columna video_url a la tabla ejercicio"""
    with engine.begin() as conn:
        try:
            # Verificar si la columna ya existe
            result = conn.execute(text("PRAGMA table_info(ejercicio)"))
            columns = [row[1] for row in result]

            if 'video_url' not in columns:
                # Agregar la columna
                conn.execute(text("ALTER TABLE ejercicio ADD COLUMN video_url VARCHAR"))
                print("✅ Columna 'video_url' agregada exitosamente a la tabla 'ejercicio'")
            else:
                print("ℹ️ La columna 'video_url' ya existe en la tabla 'ejercicio'")

        except Exception as e:
            print(f"❌ Error al agregar columna: {e}")


if __name__ == "__main__":
    add_video_url_column()