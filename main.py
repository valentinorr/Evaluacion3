from sqlalchemy import create_engine
from models import Base

DATABASE_URL = "sqlite:///restaurant.db"
engine = create_engine(DATABASE_URL)

def inicializar_db():
    print("Inicializando la base de datos...")
    Base.metadata.create_all(engine)
    print("Tablas creadas correctamente.")

if __name__ == "__main__":
    inicializar_db()
