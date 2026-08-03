from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

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

    # Relacionamento para acessar as vacinas a partir do pet
    vaccines = relationship("Vaccine", back_populates="card", cascade="all, delete-orphan")


class Vaccine(Base):
    __tablename__ = "vaccines"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_id = Column(String, ForeignKey("cat_cards.id_number"), index=True) # Vínculo com a tabela de cards
    pet_name = Column(String, nullable=False)
    vaccine_date = Column(String, nullable=False)
    vaccine_type = Column(String, nullable=False)
    photo_url = Column(String, nullable=True)

    # Relacionamento de volta para o pet
    card = relationship("CatCard", back_populates="vaccines")