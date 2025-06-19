# app/schemas/schemas.py
from pydantic import BaseModel, ConfigDict
from typing import List

class UserBase(BaseModel): #Hereda de BaseModel que proporciona validación
    username: str
    role: str

class UserCreate(UserBase): # Campos que se requieren al crear un usuario (ej. password)
    pass

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True) # Pydantic podrá usar atributos de SQLAlchemy directamente




class ChatMessageBase(BaseModel):
    message: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessage(ChatMessageBase):
    id: int
    user_id: int
    response: str

    model_config = ConfigDict(from_attributes=True)



class History(BaseModel):
    history: List[ChatMessage]
