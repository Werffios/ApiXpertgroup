# app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv() # Carga las variables de entorno desde un archivo .env y las hace disponibles en os.environ

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db") # Ya que .env está disponible, obtenemos la URL de la base de datos desde una variable de entorno, si no existe, usamos una base de datos SQLite por defecto

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Crea un generador de sesiones

Base = declarative_base() # Base para los modelos de SQLAlchemy, que se utilizará para definir las tablas de la base de datos

def get_db(): # Generador de sesiones para obtener una sesión de base de datos
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
