from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models, schemas

# Cria as tabelas no Postgres automaticamente ao iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Carteirinha")

# Libera requisições do Frontend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/card/{card_id}", response_model=schemas.CatCardResponse)
def read_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(models.CatCard).filter(models.CatCard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada")
    return card

@app.post("/api/card", response_model=schemas.CatCardResponse)
def create_card(card: schemas.CatCardBase, db: Session = Depends(get_db)):
    db_card = models.CatCard(**card.model_dump())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card