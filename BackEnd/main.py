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
@app.patch("/api/card/{card_id}/name", response_model=schemas.CatCardResponse)
def update_cat_name(card_id: str, payload: dict = Body(...), db: Session = Depends(get_db)):
    card = db.query(models.CatCard).filter(models.CatCard.id_number == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada")
    
    new_name = payload.get("name")
    if not new_name or not new_name.strip():
        raise HTTPException(status_code=400, detail="O nome não pode ser vazio")
        
    card.name = new_name.strip()
    db.commit()
    db.refresh(card)
    return card

# Rota para atualizar o cargo usando a chave id_number
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

# Rota para atualizar o nome usando a chave id_number
@app.patch("/api/card/{card_id}/breed", response_model=schemas.CatCardResponse)
def update_cat_breed(card_id: str, payload: dict = Body(...), db: Session = Depends(get_db)):
    card = db.query(models.CatCard).filter(models.CatCard.id_number == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada")
    
    new_breed = payload.get("breed")
    if not new_breed or not new_breed.strip():
        raise HTTPException(status_code=400, detail="A raça não pode ser vazia")
        
    card.breed = new_breed.strip()
    db.commit()
    db.refresh(card)
    return card

# Rota para atualizar a data de nascimento
@app.patch("/api/card/{card_id}/birth_date", response_model=schemas.CatCardResponse)
def update_cat_birth_date(card_id: str, payload: dict = Body(...), db: Session = Depends(get_db)):
    card = db.query(models.CatCard).filter(models.CatCard.id_number == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada")
    
    new_birth_date = payload.get("birth_date")
    if not new_birth_date or not new_birth_date.strip():
        raise HTTPException(status_code=400, detail="A data de nascimento não pode ser vazia")
        
    card.birth_date = new_birth_date.strip()
    db.commit()
    db.refresh(card)
    return card

# Rota para atualizar a cor
@app.patch("/api/card/{card_id}/color", response_model=schemas.CatCardResponse)
def update_cat_color(card_id: str, payload: dict = Body(...), db: Session = Depends(get_db)):
    card = db.query(models.CatCard).filter(models.CatCard.id_number == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada")
    
    new_color = payload.get("color")
    if not new_color or not new_color.strip():
        raise HTTPException(status_code=400, detail="A cor não pode ser vazia")
        
    card.color = new_color.strip()
    db.commit()
    db.refresh(card)
    return card

# Rota para atualizar o Tutor 1
@app.patch("/api/card/{card_id}/owner", response_model=schemas.CatCardResponse)
def update_cat_owner(card_id: str, payload: dict = Body(...), db: Session = Depends(get_db)):
    card = db.query(models.CatCard).filter(models.CatCard.id_number == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada")
    
    new_owner = payload.get("owner", "")
    card.owner = new_owner.strip()
    db.commit()
    db.refresh(card)
    return card

# Rota para atualizar o Tutor 2
@app.patch("/api/card/{card_id}/second_owner", response_model=schemas.CatCardResponse)
def update_cat_second_owner(card_id: str, payload: dict = Body(...), db: Session = Depends(get_db)):
    card = db.query(models.CatCard).filter(models.CatCard.id_number == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada")
    
    new_second_owner = payload.get("second_owner", "")
    card.second_owner = new_second_owner.strip()
    db.commit()
    db.refresh(card)
    return card

# Rota para atualizar o superpoder
@app.patch("/api/card/{card_id}/superpower", response_model=schemas.CatCardResponse)
def update_cat_superpower(card_id: str, payload: dict = Body(...), db: Session = Depends(get_db)):
    card = db.query(models.CatCard).filter(models.CatCard.id_number == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada")
    
    new_superpower = payload.get("superpower", "")
    card.superpower = new_superpower.strip()
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