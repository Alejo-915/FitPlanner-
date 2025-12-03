from sqlmodel import SQLModel
from db import engine
from models import Objetivo

def create_objetivo_table():
    # Esto creará solo las tablas que no existen, en este caso 'objetivo'
    SQLModel.metadata.create_all(engine)
    print("Tabla 'objetivo' creada exitosamente.")

if __name__ == "__main__":
    create_objetivo_table()
