from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# String de conexão com o Postgres local do Docker
DATABASE_URL = "postgresql://postgres:Projeto_carteirinha@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency para injetar a sessão do banco nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()