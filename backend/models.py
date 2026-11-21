from datetime import datetime, timezone
import uuid
from sqlalchemy import ForeignKey, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

def utcnow():
    return datetime.now(timezone.utc)

class Book(Base):
    __tablename__ = "books"
    id : Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200)) 
    author: Mapped[str] = mapped_column(String(200))
    genre: Mapped[str] = mapped_column(String(200))
    price: Mapped[float]
    stock: Mapped[int] = mapped_column(default=0)
    description: Mapped[str] = mapped_column(Text)

class Policy(Base):
    __tablename__ = "policy"
    id: Mapped[int] = mapped_column(primary_key=True)
    topic: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)

class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_number: Mapped[str] = mapped_column(String(50), unique=True)
    customer_phone: Mapped[str] = mapped_column(String(30))
    shipping_status: Mapped[str]

class Conversation(Base):
    __tablename__ = "conversation"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    need_human: Mapped[bool] = mapped_column(default=False)

class Messages(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversation.id"))
    role: Mapped[str]
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    quantity: Mapped[int] = mapped_column(default=1)

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    casdoor_id: Mapped[str] = mapped_column(String(36), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)