from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL de la base de datos
DATABASE_URL = "sqlite:///restaurant.db"

# Creación del motor de base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Configuración del generador de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
