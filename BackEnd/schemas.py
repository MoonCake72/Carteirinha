from pydantic import BaseModel

class CatCardBase(BaseModel):
    name: str
    title: str
    id_number: str
    breed: str
    birth_date: str
    color: str
    owner: str
    superpower: str
    favorite_food: str

class CatCardResponse(CatCardBase):
    id: int

    class Config:
        from_attributes = True


