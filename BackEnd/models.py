from sqlalchemy import Column, Integer ,String
from database import Base

class CatCard(Base):
    __tablename__ = "cat_cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    id_number = Column(String, unique=True, nullable=False)
    breed = Column(String, default="SRD")
    birth_date = Column(String)
    color = Column(String)
    owner = Column(String)
    superpower = Column(String)
    favorite_food = Column(String)