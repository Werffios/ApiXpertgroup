# app/db/crud.py
from sqlalchemy.orm import Session
from app.db import models  # Importa los modelos de la base de datos (messages, users)
from app.schemas import schemas
from typing import List


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_chat_message(db: Session, item: schemas.ChatMessageCreate, user_id: int, response: str):
    db_item = models.ChatMessage(**item.model_dump(), user_id=user_id, response=response)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_chat_messages_by_user(db: Session, user_id: int) -> List[schemas.ChatMessage]:
    history = []
    for content in db.query(models.ChatMessage).filter(models.ChatMessage.user_id == user_id).all():
        history.append(schemas.ChatMessage(
            id=content.id,
            user_id=content.user_id,
            message=content.message,
            response=content.response
        ))
    return history
