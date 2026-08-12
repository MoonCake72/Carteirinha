from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    cat_cards = relationship("CatCard", back_populates="user")


class CatCard(Base):
    __tablename__ = "cat_cards"

    id_number = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    breed = Column(String, default="SRD")
    birth_date = Column(String)
    color = Column(String)
    owner = Column(String)                           
    second_owner = Column(String, nullable=True, default="")
    superpower = Column(String)
    favorite_food = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="cat_cards")
    vaccines = relationship("Vaccine", back_populates="card", cascade="all, delete-orphan")


class Vaccine(Base):
    __tablename__ = "vaccines"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_id = Column(String, ForeignKey("cat_cards.id_number"), index=True) # Vínculo com a tabela de cat_cards
    pet_name = Column(String, nullable=False)
    vaccine_date = Column(String, nullable=False)
    vaccine_type = Column(String, nullable=False)
    next_date = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    card = relationship("CatCard", back_populates="vaccines")