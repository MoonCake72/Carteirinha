import os
import shutil
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Body, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models, schemas

# Cria a tabela no banco caso ainda não exista
Base.metadata.create_all(bind=engine)

# Cria o diretório para armazenar os comprovantes caso não exista
UPLOAD_DIR = "uploads/vaccines"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="API Carteirinha")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir os arquivos estáticos de upload
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# ------------------- ROTAS DA CARTEIRINHA PET -------------------

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

# Rota para atualizar a raça
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

# Rota para atualizar a comida favorita
@app.patch("/api/card/{card_id}/favorite_food", response_model=schemas.CatCardResponse)
def update_cat_favorite_food(card_id: str, payload: dict = Body(...), db: Session = Depends(get_db)):
    card = db.query(models.CatCard).filter(models.CatCard.id_number == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada")
    
    new_favorite_food = payload.get("favorite_food", "")
    card.favorite_food = new_favorite_food.strip()
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


# ------------------- ROTAS DE VACINAS -------------------

# 1. GET: Listar vacinas incluindo next_date
@app.get("/api/card/{card_id}/vaccines", response_model=List[schemas.VaccineResponse])
def get_vaccines(card_id: str, db: Session = Depends(get_db)):
    card = db.query(models.CatCard).filter(models.CatCard.id_number == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada")
        
    vaccines = db.query(models.Vaccine).filter(models.Vaccine.card_id == card_id).order_by(models.Vaccine.id.desc()).all()
    
    return [
        {
            "id": v.id,
            "card_id": v.card_id,
            "date": v.vaccine_date,
            "type": v.vaccine_type,
            "next_date": v.next_date,
            "photo_url": v.photo_url
        } for v in vaccines
    ]

# 2. POST: Adicionar vacina recebendo next_date
@app.post("/api/card/{card_id}/vaccines", response_model=schemas.VaccineResponse)
async def add_vaccine(
    card_id: str,
    date: str = Form(...),
    type: str = Form(...),
    next_date: Optional[str] = Form(None),  # <-- Recebe a próxima data (ou None)
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    card = db.query(models.CatCard).filter(models.CatCard.id_number == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada")

    saved_photo_url = None

    if photo and photo.filename:
        file_extension = os.path.splitext(photo.filename)[1]
        filename = f"{card_id}_{os.urandom(8).hex()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        
        saved_photo_url = f"http://127.0.0.1:8000/uploads/vaccines/{filename}"

    new_vaccine = models.Vaccine(
        card_id=card_id,
        pet_name=card.name,
        vaccine_date=date.strip(),
        vaccine_type=type.strip(),
        next_date=next_date.strip() if next_date else None,
        photo_url=saved_photo_url
    )
    db.add(new_vaccine)
    db.commit()
    db.refresh(new_vaccine)

    return {
        "id": new_vaccine.id,
        "card_id": new_vaccine.card_id,
        "date": new_vaccine.vaccine_date,
        "type": new_vaccine.vaccine_type,
        "next_date": new_vaccine.next_date,
        "photo_url": new_vaccine.photo_url
    }

# 3. Remover uma vacina específica
@app.delete("/api/card/{card_id}/vaccines/{vaccine_id}")
def delete_vaccine(card_id: str, vaccine_id: int, db: Session = Depends(get_db)):
    vaccine = db.query(models.Vaccine).filter(
        models.Vaccine.id == vaccine_id, 
        models.Vaccine.card_id == card_id
    ).first()
    
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vacina não encontrada para esta carteirinha")
        
    db.delete(vaccine)
    db.commit()
    return {"message": "Vacina removida com sucesso"}

# 4. Limpar todo o histórico de vacinas do pet
@app.delete("/api/card/{card_id}/vaccines")
def clear_vaccines(card_id: str, db: Session = Depends(get_db)):
    db.query(models.Vaccine).filter(models.Vaccine.card_id == card_id).delete()
    db.commit()
    return {"message": "Histórico de vacinas limpo com sucesso"}