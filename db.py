from sqlmodel import SQLModel, create_engine, Session
import os

# Leer la URL de la base de datos desde las variables de entorno
# o usar SQLite localmente si no está configurada
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///fitplanner.db"  # Fallback para desarrollo local
)

# PostgreSQL requiere usar 'postgresql://' en lugar de 'postgres://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configuración del engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  # Verifica las conexiones antes de usarlas
    pool_recycle=300     # Recicla conexiones cada 5 minutos
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
