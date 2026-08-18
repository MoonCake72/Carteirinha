import os
import shutil
import random
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Body, File, UploadFile, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session
from sqlalchemy import text
from jose import jwt, JWTError

from database import engine, Base, get_db
import models, schemas, security

# Cria as tabelas no banco caso ainda não existam
Base.metadata.create_all(bind=engine)

# Cria o diretório para armazenar os comprovantes caso não exista
UPLOAD_DIR = "uploads/vaccines"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="API Carteirinha")

# Configuração do CORS
origins = [
    "https://mooncake72.github.io",  # Seu site oficial em produção
    "http://localhost:5500",          # Testes locais (Live Server)
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir os arquivos estáticos de upload
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Scheme de segurança para autenticação via Bearer Token JWT
security_scheme = HTTPBearer()

# ----------------- FUNÇÕES AUXILIARES / SEGURANÇA -----------------

def generate_card_id() -> str:
    """Gera um identificador único para o cartão (ex: '4821-GATA')."""
    random_num = random.randint(1000, 9999)
    return f"{random_num}-GATA"


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> int:
    """Extrai e valida o ID do usuário de dentro do Token JWT enviado no Header."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token inválido"
            )
        return int(user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token inválido ou expirado"
        )


# ----------------- ROTAS DE AUTENTICAÇÃO -----------------

@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Verifica se o e-mail já está cadastrado
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado."
        )

    # 2. Criptografa a senha e cria o novo usuário
    hashed_pwd = security.hash_password(user_data.password)
    new_user = models.User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 3. Gera a carteirinha em branco vinculada a este novo usuário
    new_card_id = generate_card_id()

    blank_card = models.CatCard(
        id_number=new_card_id,
        name="",                 # Em branco para o tutor preencher depois
        title="",
        breed="SRD",
        birth_date="",
        color="",
        owner=new_user.name,     # Nome do tutor obtido do cadastro
        second_owner="",
        superpower="",
        favorite_food="",
        user_id=new_user.id      # Vincula ao ID do usuário criado
    )

    db.add(blank_card)
    db.commit()

    return {
        "message": "Usuário e carteirinha criados com sucesso!",
        "user_id": new_user.id,
        "card_id": new_card_id
    }


@app.post("/api/auth/login", response_model=schemas.Token)
def login_user(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    # 1. Busca usuário pelo e-mail
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )

    # 2. Valida a senha digitada
    if not security.verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )

    # 3. Gera o Token JWT
    access_token = security.create_access_token(data={"sub": str(user.id), "email": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_name": user.name
    }


@app.delete("/api/auth/users/by-email/{email}", status_code=status.HTTP_200_OK)
def delete_user_by_email(email: str, db: Session = Depends(get_db)):
    # Deleta diretamente na tabela users via SQL puro para testes
    result = db.execute(text("DELETE FROM users WHERE email = :email"), {"email": email})
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )

    return {"message": f"Usuário {email} foi removido com sucesso!"}


# ------------------- ROTAS DA CARTEIRINHA PET -------------------

# Rota para buscar a carteirinha do usuário logado (Autenticado)
@app.get("/api/my-card", response_model=schemas.CatCardResponse)
def get_my_cat_card(
    user_id: int = Depends(get_current_user_id), 
    db: Session = Depends(get_db)
):
    card = db.query(models.CatCard).filter(models.CatCard.user_id == user_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada.")
    return card


# Rota para buscar o cartão pelo id_number (Pública / Leitura)
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


# Rota para criar cartão manualmente
@app.post("/api/card", response_model=schemas.CatCardResponse)
def create_card(card: schemas.CatCardBase, db: Session = Depends(get_db)):
    db_card = models.CatCard(**card.model_dump())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


# ------------------- ROTAS DE VACINAS -------------------

# 1. GET: Listar vacinas buscando pelo id_number do cartão
@app.get("/api/card/{card_id}/vaccines", response_model=List[schemas.VaccineResponse])
def get_vaccines(card_id: str, db: Session = Depends(get_db)):
    card = db.query(models.CatCard).filter(models.CatCard.id_number == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada")
        
    # Filtra as vacinas diretamente pelo id_number do cartão
    vaccines = db.query(models.Vaccine).filter(models.Vaccine.card_id == card_id).order_by(models.Vaccine.id.desc()).all()
    
    return [
        {
            "id": v.id,
            "card_id": v.card_id,
            "date": getattr(v, 'vaccine_date', None) or getattr(v, 'application_date', ''),
            "type": getattr(v, 'vaccine_type', None) or getattr(v, 'vaccine_name', ''),
            "next_date": getattr(v, 'next_date', None) or getattr(v, 'next_due_date', None),
            "photo_url": getattr(v, 'photo_url', None)
        } for v in vaccines
    ]


# 2. POST: Adicionar vacina buscando a carteirinha pelo id_number
@app.post("/api/card/{card_id}/vaccines", response_model=schemas.VaccineResponse)
async def add_vaccine(
    card_id: str,
    date: str = Form(...),
    type: str = Form(...),
    next_date: Optional[str] = Form(None),
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
        
        saved_photo_url = f"/uploads/vaccines/{filename}"

    # Instancia usando os nomes corretos dos atributos do modelo Vaccine
    new_vaccine = models.Vaccine(
        card_id=card_id,
        pet_name=card.name or "",
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
    card = db.query(models.CatCard).filter(models.CatCard.id_number == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada")

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
    card = db.query(models.CatCard).filter(models.CatCard.id_number == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carteirinha não encontrada")

    db.query(models.Vaccine).filter(models.Vaccine.card_id == card_id).delete()
    db.commit()
    return {"message": "Histórico de vacinas limpo com sucesso"}