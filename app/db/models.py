# app/db/models.py
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base  # Importa la clase Base desde database.py, será la base para los modelos de SQLAlchemy


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    role: Mapped[str] = mapped_column()
    # HasMany
    messages: Mapped[list["ChatMessage"]] = relationship(back_populates="owner")  # Establece una relación con ChatMessage


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    message: Mapped[str] = mapped_column()
    response: Mapped[str] = mapped_column()
    # BelongsTo
    owner: Mapped["User"] = relationship(back_populates="messages")  # Establece una relación con User
