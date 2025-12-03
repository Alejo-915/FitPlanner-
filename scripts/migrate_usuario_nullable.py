from sqlalchemy import text
from db import engine


def migrate_usuario_nullable():
    with engine.begin() as conn:
        conn.execute(text("PRAGMA foreign_keys=OFF;"))
        conn.execute(text("DROP TABLE IF EXISTS usuario_new;"))

        conn.execute(
            text(
                """
                CREATE TABLE usuario_new (
                    id INTEGER PRIMARY KEY,
                    nombre VARCHAR NOT NULL,
                    correo VARCHAR NOT NULL,
                    "contraseña" VARCHAR NOT NULL,
                    edad INTEGER NOT NULL,
                    peso REAL,
                    altura REAL,
                    objetivo VARCHAR NOT NULL,
                    activo BOOLEAN NOT NULL
                )
                """
            )
        )

        table_exists = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='usuario';")
        ).first()

        if table_exists:
            conn.execute(
                text(
                    """
                    INSERT INTO usuario_new (id, nombre, correo, "contraseña", edad, peso, altura, objetivo, activo)
                    SELECT id, nombre, correo, "contraseña", edad, peso, altura, objetivo, activo FROM usuario;
                    """
                )
            )
            conn.execute(text("DROP TABLE usuario;"))

        conn.execute(text("ALTER TABLE usuario_new RENAME TO usuario;"))
        conn.execute(text("PRAGMA foreign_keys=ON;"))


if __name__ == "__main__":
    migrate_usuario_nullable()
    print("Migración completada: columnas peso y altura ahora permiten NULL.")
