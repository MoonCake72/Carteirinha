from pydantic import BaseModel
from typing import Optional

# --- SCHEMAS DO CARTÃO PET ---
class CatCardBase(BaseModel):
    id_number: str
    name: str
    title: str
    breed: str
    birth_date: str
    color: str
    owner: str
    second_owner: Optional[str] = ""
    superpower: str
    favorite_food: str

class CatCardResponse(CatCardBase):
    class Config:
        from_attributes = True


# --- SCHEMAS DE VACINAS ---
class VaccineCreate(BaseModel):
    date: str
    type: str

class VaccineResponse(BaseModel):
    id: int
    card_id: str
    date: str
    type: str

    class Config:
        from_attributes = True