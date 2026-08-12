from pydantic import BaseModel, EmailStr
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
    next_date: Optional[str] = None
    photo_url: Optional[str] = None
    
    class Config:
        from_attributes = True
    
# --- SCHEMAS DE PARA CADASTRO DE USUÁRIOS ---
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

# Schema para login
class UserLogin(BaseModel):
    email: str
    password: str

# Schema de resposta após login
class Token(BaseModel):
    access_token: str
    token_type: str
    user_name: str
