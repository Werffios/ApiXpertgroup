#app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db import crud
from app.schemas import schemas
from app.db.database import get_db
from app.services import openai_service

router = APIRouter()

@router.post("/init_user", response_model=schemas.User)
def init_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe!")
    return crud.create_user(db=db, user=user)

@router.post("/ask")
def ask(message: schemas.ChatMessageCreate, username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="El usuario no existe!")

    response = openai_service.get_chatbot_response(str(db_user.role), message.message)

    chat_message = schemas.ChatMessageCreate(message=message.message)
    crud.create_chat_message(db=db, item=chat_message, user_id=int(db_user.id), response=response)

    return {"response": response}

@router.get("/history/{username}", response_model=schemas.History)
def get_history(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="El usuario no existe!")

    history = crud.get_chat_messages_by_user(db, user_id=int(db_user.id))
    return {"history": history}

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Check database connection
        db.execute(text("SELECT 1"))
        db_status = "Todo bien, todo ok!"
    except Exception as e:
        db_status = "error: " + str(e)

    return {"service_status": "OK", "database_status": db_status}
