from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

# Configuração do hash de senha com bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Chave secreta para assinar os tokens JWT (pode alterar para uma frase sua)
SECRET_KEY = "carteirinha_pet_chave_secreta_super_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # Token válido por 24 horas

def hash_password(password: str) -> str:
    """Gera o hash da senha usando bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara a senha digitada com o hash salvo no banco."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """Gera um Token JWT de acesso."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt