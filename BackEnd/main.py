from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Carteirinha")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota para buscar o cartão pelo id_number
@app.get("/api/card/{card_id}", response_model=schemas.CatCardResponse)
def read_card(card_id: str, db: Session = Depends(get_db)):
    card = db.query(models.CatCard).filter(models.CatCard.id_number == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada")
    return card

# Rota para atualizar o nome usando a chave id_number
@app.patch("/api/card/{card_id}/title", response_model=schemas.CatCardResponse)
def update_cat_title(card_id: str, payload: dict = Body(...), db: Session = Depends(get_db)):
    card = db.query(models.CatCard).filter(models.CatCard.id_number == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada")
    
    new_title = payload.get("title")
    if not new_title or not new_title.strip():
        raise HTTPException(status_code=400, detail="O cargo não pode ser vazio")
        
    card.title = new_title.strip()
    db.commit()
    db.refresh(card)
    return card

# Rota para criar cartão
@app.post("/api/card", response_model=schemas.CatCardResponse)
def create_card(card: schemas.CatCardBase, db: Session = Depends(get_db)):
    db_card = models.CatCard(**card.model_dump())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card