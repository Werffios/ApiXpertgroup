# main.py
from fastapi import FastAPI
from app.api import routes
from app.db import models
from app.db.database import engine

models.Base.metadata.create_all(bind=engine) # Crea las tablas en la base de datos si no existen

app = FastAPI()

app.include_router(routes.router)
