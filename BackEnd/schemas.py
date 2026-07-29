from pydantic import BaseModel

class CatCardBase(BaseModel):
    id_number: str
    name: str
    title: str
    breed: str
    birth_date: str
    color: str
    owner: str
    superpower: str
    favorite_food: str

class CatCardResponse(CatCardBase):
    class Config:
        from_attributes = True